from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from agno.agent import Agent, RunResponse
from agno.team.team import Team
from agno.tools.youtube import YouTubeTools
from agno.models.groq import Groq

# Initialize the FastAPI app
app = FastAPI(
    title="YouTube Content Processing Team API",
    description="Transforms a YouTube video into a validated, engaging Markdown blog post using a multi‑agent workflow.",
    version="1.0"
)
# Cors
# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize the YouTube transcription tool
yt_tool = YouTubeTools()

# Define the shared language model for your agents
shared_model = Groq(
    id="llama-3.1-8b-instant",
    api_key="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"
)

# Function to transcribe YouTube video
def transcribe_youtube_video(video_url: str) -> str:
    """Retrieves captions from a YouTube video."""
    captions = yt_tool.get_youtube_video_captions(video_url)
    if not captions:
        captions = "❌ No captions available for this video."
    return captions

# Agent 1: Blog Writing Agent
blog_writer_agent = Agent(
    name="Blog Writer Agent",
    role="Generate a high-quality blog post based on the transcribed video content.",
    model=shared_model,
    show_tool_calls=True,
    description=(
        "Transforms the transcription into a structured, engaging and eye-catching storytelling blog post."
    ),
)

# Agent 2: Content Validation Agent
validation_agent = Agent(
    name="Validation Agent",
    role="Ensure the blog post accurately represents the video transcript.",
    model=shared_model,
    show_tool_calls=True,
    description="Checks the blog post for accuracy and assigns necessary edits.",
)

# Multi-Agent Team (primarily for internal workflow documentation)
content_creation_team = Team(
    name="YouTube Content Processing Team",
    mode="route",
    model=shared_model,
    members=[blog_writer_agent, validation_agent],
    show_tool_calls=True,
    markdown=True,
    description=(
        "Processes YouTube videos into validated blog posts using a structured workflow."
    ),
    instructions=[
        "Step 1: Transcribe the YouTube video using YouTubeTools.",
        "Step 2: Pass the transcription to the blog writer agent to generate an article.",
        "Step 3: Validate the generated blog post using the validation agent.",
        "If the validation agent finds issues, automatically send those improvements "
        "back to the blog writer agent.",
        "Ensure the final validated blog post aligns with the transcription before displaying.",
    ],
    show_members_responses=True,
)

# Pydantic request model
class VideoRequest(BaseModel):
    url: str

@app.post("/generate-blog", summary="Generate a validated Markdown blog post from a YouTube Video")
async def generate_blog(request: VideoRequest):
    video_url = request.url

    # Step 1: Transcribe the YouTube video
    try:
        transcription_response = transcribe_youtube_video(video_url)
        if not transcription_response:
            raise ValueError("Empty transcription received.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving transcription: {str(e)}")
    
    # Step 2: Generate a blog post from the transcript
    try:
        blog_response = blog_writer_agent.run(
            f"Write a blog post based on the transcript:\n{transcription_response}",
            markdown=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog post: {str(e)}")
    
    # Step 3: Validate the generated blog post
    try:
        validation_response = validation_agent.run(
            f"Check if this blog post correctly represents the transcription:\n{blog_response.content}",
            markdown=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during validation: {str(e)}")
    
    final_blog = blog_response.content

    # Step 4: If enhancements are needed, revise the blog post
    if "Enhancements needed" in validation_response.content:
        try:
            revised_blog_response = blog_writer_agent.run(
                f"Improve the blog post based on these suggestions:\n{validation_response.content}",
                markdown=True,
            )
            # Final validation step (optional)
            final_validation = validation_agent.run(
                f"Final check on revised blog post:\n{revised_blog_response.content}",
                markdown=True,
            )
            final_blog = revised_blog_response.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during blog post revision: {str(e)}")
    
    # Return the final validated blog post in Markdown format
    return {"blog_post": final_blog}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)