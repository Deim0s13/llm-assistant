# LLM Chatbot Start Kit

This project is a starting point for building an LLM-based chatbot using the '"03-mini-high"' model. It leverages Hugging Face's Transformers and Gradio to create a simple chat interface.

## Setup

1. **Create and activate a virtual enviornment:**

   ```bash
   python3 -m venv env
   source env/bin/activate

2. **Install dependences:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

3. **Run the chatbot:**

   ```bash
   python main.py

The app should open a browser window with the Gradio interface

## Next Steps

- Experiment with generation parameters and prompt engineering.
- Expand the chat function to handle conversation histroy.
- Containerise the application by using Podman for deployment
