import subprocess
import gradio as gr
import os
import tempfile
import shutil
import time


def convert(url: str):
    if not url:
        return None

    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, "input.m4a")

    os.makedirs("output", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = f"lofi_{timestamp}.mp3"
    output_path = os.path.join("output", output_filename)

    try:
        # Download audio using yt-dlp
        yt_dlp_command = [
            "yt-dlp",
            "-f", "bestaudio[ext=m4a]",
            "-o", input_path,
            url
        ]
        result = subprocess.run(yt_dlp_command, capture_output=True, text=True, check=True)

        # Apply ffmpeg filter chain
        ffmpeg_filter_chain = "atempo=0.9,lowpass=f=5000,highpass=f=150,aecho=0.8:0.9:1000:0.3"
        ffmpeg_command = [
            "ffmpeg",
            "-i", input_path,
            "-af", ffmpeg_filter_chain,
            output_path
        ]
        result = subprocess.run(ffmpeg_command, capture_output=True, text=True, check=True)

        return output_path
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def main():
    with gr.Blocks(title="YouTube to Lofi Converter") as demo:
        gr.Markdown("# YouTube to Lofi Converter")
        url_in = gr.Textbox(label="YouTube URL")
        convert_btn = gr.Button("Convert")
        audio_out = gr.Audio(label="Lofi Output")

        convert_btn.click(fn=convert, inputs=url_in, outputs=audio_out)
    demo.launch()


if __name__ == "__main__":
    main()
