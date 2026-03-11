import gradio as gr
from helper import predict_digit

# --- 5. Build and Launch the Web UI ---
print("Launching Gradio UI...")

demo = gr.Interface(
    fn=predict_digit,
    inputs=gr.Sketchpad(crop_size=(28, 28), type="numpy", image_mode="L"),
    outputs=gr.Label(num_top_classes=3),
    title="PyTorch MNIST Recognizer",
    description="Draw a single number (0-9) on the canvas below and watch the AI guess!"
)

# Launch with a public link
demo.launch(share=True)