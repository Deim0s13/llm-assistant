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

def chat(message, history):
    """
    Build a conversation context history, generate a response, and return the updated history.
    """
    # Construct the prompt by iterating over history
    context = ""
    for user_msg, bot_msg in history:
        context += f"User: {user_msg}\nBot: {bot_msg}\n"
    # Add the latest user message
    context += f"User: {message}\nBot: "

    # Encode the context and generate a response
    input_ids = tokenizer.encode(context, return_tensors="pt").to(device)
    # Set max-length relative to imput length (adjust as needed)
    max_length = input_ids.shape[1] +50
    output_ids = model.generate(
        input_ids,
        max_length=max_length,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Remove the prompt portion from the generated text
    new_response = output_text[len(context):].strip()
    #If the model continues with a new user turn, cut off at "User:"
    if "User:" in new_response:
        new_response = new_response.split("User:")[0].strip()

    # Update the conversation history with the new exchange
    history.append((message, new_response))
    return history

def respond(message, history):
    """
    Wrapper function for Gradio: receives a new message and current history, updates the history with the new exchange, and returns an empty string to clear the input.
    """
    history = history or []
    updated_history = chat(message, history)
    return "", updated_history

# Create a Gradio interface with using Blocks with a ChatBot component
with gr.Blocks() as demo:
    gr.Markdown("# Enhanced Chatbot with Conversation Context")
    chatbot = gr.Chatbot()
    state = gr.State([]) # This holds the conversation history
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter your message and press Enter").style(container=False)
    # When the user submits a message, call 'respond'
    txt.submit(respond, [txt, state], [txt, chatbot])

demo.launch()