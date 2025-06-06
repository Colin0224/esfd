# YouTube to Lofi Converter

This project provides a simple web interface that converts a YouTube video to a lofi-style MP3.

## Requirements

- Python 3.9+
- Go 1.18+
- [FFmpeg](https://ffmpeg.org/) installed and available in `PATH`
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) installed and available in `PATH`
- Python package `gradio`

## Building the Go backend

```
go build -o lofi-converter lofi_converter.go
```

## Running the web app

First, install Python dependencies:

```
pip install gradio
```

Then launch the Gradio interface:

```
python app.py
```

Paste a YouTube URL in the input field and press **Convert** to generate the lofi audio.
