# BlogGenius: YouTube to Blog Generator

Convert any YouTube video into a professionally written, well-structured blog post with our AI-powered tool.

## Features

- **AI-Powered Blog Generation**: Transform YouTube videos into engaging blog posts
- **Professional UI**: Clean and intuitive interface for both light and dark modes
- **One-Click Generation**: Simply paste a YouTube URL and get a fully-formatted blog post
- **Easy Export**: Download your blog in Markdown format
- **History Tracking**: Keep track of all your generated blog posts

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bloggenius.git
   cd bloggenius
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your environment:
   Make sure you have the required API keys set up for the Groq API as used in the Blog.py file.

## Usage

### Option 1: Run Everything with a Single Command

The easiest way to start BlogGenius is with our run script:

```
python run.py
```

This will start both the FastAPI backend and Streamlit frontend, and automatically open your browser to the application interface.

### Option 2: Running Components Separately

If you prefer to run the components separately:

#### Running the API Server

Start the FastAPI server:

```
python -m uvicorn Blog:app --host 0.0.0.0 --port 8000
```

#### Running the Streamlit UI

In a separate terminal, run the Streamlit app:

```
streamlit run streamlit_app.py
```

Then open your browser at http://localhost:8501 to use the application.

## Architecture

- **Blog.py**: FastAPI backend that handles video transcription and blog generation using the agno library
- **streamlit_app.py**: Streamlit-based frontend with an attractive, responsive UI
- **run.py**: Helper script to run both components together

## Technical Details

The application uses:
- **FastAPI** for the backend API
- **Streamlit** for the frontend UI
- **Agno** for YouTube transcription and AI blog generation
- **Groq** for the large language model powering the blog generation

## License

MIT

## Credits

Created with ❤️ using:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Groq AI](https://groq.com/)
- [agno](https://github.com/agno) 