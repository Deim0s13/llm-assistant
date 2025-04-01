from transformers import AutoTokenizer, AutoModelForCausalLM
import gradio as gr
import torch

# Define your model name
model_name = "distilgpt2"

# Load tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Use Apple's MPS backend if available, else default to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)

def chat(message):
    """
    Simple chat function that takes a message, generates a response, and returns it.
    """
    input_ids = tokenizer.encode(message, return_tensors="pt").to(device)

    # Generate a response (adjust parameters as needed)
    output_ids = model.generate(
        input_ids,
        max_length=150,
        do_sample=True,
        temprature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

# Create a Gradio interface for interaction
iface = gr.Interface(fn=chat, inputs="text", outputs="text", title="03-mini-high Chatbot")

if __name__ == "__main__":
    iface.launch()