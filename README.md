# Sift

Sift is an AI-powered tool that extracts concise insights and summaries
from YouTube videos. It uses a hybrid NLP pipeline combining semantic
extraction and transformer-based abstractive summarization to generate
structured summaries of long-form video content.

The system is designed to reduce hallucination, improve relevance, and
make long videos quickly digestible.

------------------------------------------------------------------------

## Features

-   Summarizes YouTube videos using their transcripts
-   Hybrid summarization pipeline:
    -   Semantic extractive filtering using Sentence-BERT
    -   Abstractive summarization using transformer models
-   Structured output including:
    -   Title
    -   Key points
    -   Short summary
    -   Full summary
-   Adjustable summary length (`short`, `medium`, `long`)
-   Token-aware chunking to handle long transcripts
-   Modular NLP pipeline architecture

------------------------------------------------------------------------

## Architecture

Pipeline overview:

YouTube Video\
↓\
Transcript Retrieval\
↓\
Text Preprocessing\
↓\
Semantic Sentence Extraction (Sentence-BERT)\
↓\
Token-aware Chunking\
↓\
Transformer Summarization\
↓\
Structured JSON Output

### Core Components

  -----------------------------------------------------------------------
  Module                              Responsibility
  ----------------------------------- -----------------------------------
  preprocessor.py                     Cleans transcript text

  semantic_extractor.py               Extracts important sentences using
                                      embeddings

  summarizer.py                       Handles chunking and transformer
                                      summarization

  app.py                              Flask API serving summaries
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Tech Stack

-   Python
-   Flask
-   HuggingFace Transformers
-   Sentence Transformers
-   Scikit-learn
-   PyTorch

------------------------------------------------------------------------

## Installation

Clone the repository:

git clone https://github.com/yourusername/sift.git\
cd sift

Create a virtual environment:

python -m venv venv

Activate the environment (Windows Git Bash):

source venv/Scripts/activate

Install dependencies:

pip install -r requirements.txt

------------------------------------------------------------------------

## Running the Server

Start the backend server:

python backend/app.py

The API will run on:

http://127.0.0.1:5000

------------------------------------------------------------------------

## API Usage

Summarize a YouTube video:

GET /summarize?video_id=`<VIDEO_ID>`{=html}

Example:

http://127.0.0.1:5000/summarize?video_id=dQw4w9WgXcQ

### Optional Parameters

Adjust summary length:

length=short\
length=medium\
length=long

Example:

http://127.0.0.1:5000/summarize?video_id=dQw4w9WgXcQ&length=long

------------------------------------------------------------------------

## Example Output

{ "title": "Key Insights From The Video", "key_points": \[ "Main concept
discussed in the video", "Important supporting idea", "Additional
insight"\], "short_summary": "Brief overview of the video.",
"full_summary": "Full structured summary of the video." }

------------------------------------------------------------------------

## Challenges Solved

-   Handling long transcripts exceeding transformer token limits
-   Reducing hallucination through semantic extraction
-   Improving summary relevance using hybrid summarization
-   Efficiently chunking large transcripts for transformer inference

------------------------------------------------------------------------

## Future Improvements

-   Chrome extension integration
-   Caching layer for repeated requests
-   GPU acceleration
-   Topic detection and tagging
-   Question answering over video transcripts

------------------------------------------------------------------------

## License

MIT License
