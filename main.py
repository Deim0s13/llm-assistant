from transformers import AutoTokenizer, AutoModelForCausalLM
import gradio as gr
import torch

# Use an instruction-tuned model: google/flan-t5-small
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Use Apple's MPS backend if available, else default to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)

def chat(message, history):
    # Build a prompt with conversation history using consistent labels.
    if not history:
        # Start with a detailed system prompt to guide responses.
        context = (
            "You are a helpful assistant that responds in English. "
            "Provide clear, detailed answers to user queries. "
            "When a user asks 'What topics can you help with?', respond with: "
            "'I can help you with topics such as technology, science, history, art, literature, and more.'"
        )

    else:
        context = ""

    # Append previous conversation turns.
    for entry in history:
        if entry["role"] == "user":
            context += f"\nUser: {entry['content']}"
        elif entry["role"] == "assistant":
            context += f"\nAssistant: {entry['content']}"
    
    # Add the current user message.
    context += f"\nUser: {message}\nAssistant: "

    # Debug Print full context
    print("DEBUG: Full context sent to model")
    print(context)

    # Tokenise with padding and get attention mask.
    encoded_input = tokenizer(context, return_tensors="pt", padding=True, truncation=True)
    input_ids = encoded_input.input_ids.to(device)

    # Generate the response.
    generation_params = {
        "max_new_tokens": 100,
        "do_sample": True,
        "temperature": 0.5,
        "top_p": 0.9,
    }

    output_ids = model.generate(input_ids, **generation_params)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Debug: Print the full generated output.
    print("DEBUG: Full generated output:")
    print(output_text)

    # For seq2seq models like T5, the output is generally a new response.
    new_response = output_text.strip()
    print("DEBUG: Extracted new response:")
    print(new_response)

    # Update conversation history with dictionary messages.
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": new_response})

    return history

def respond(message, history):
    history = history or []
    updated_history = chat(message, history)
    return "", updated_history

# Create a Gradio interface with using Blocks with a ChatBot component
with gr.Blocks() as demo:
    gr.Markdown("# Enhanced Chatbot with Conversation Context")
    chatbot = gr.Chatbot(type="messages")
    state = gr.State([]) # Holds conversation history as a list of dictionaries.
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter your message and press Enter")
    txt.submit(respond, [txt, state], [txt, chatbot])

demo.launch(share=True)