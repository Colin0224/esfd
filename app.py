import subprocess
import gradio as gr


def convert(url: str):
    if not url:
        return None
    try:
        result = subprocess.run([
            './lofi-converter', url
        ], capture_output=True, text=True, check=True)
        output_path = result.stdout.strip().splitlines()[-1]
        return output_path
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


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
