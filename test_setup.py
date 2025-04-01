import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Check if MPS is available
print("MPS available:", torch.backends.mps.is_available())

# Load a small model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.to("mps" if torch.backends.mps.is_available() else "cpu")

# Generate a test response
input_text = "Hello, how are you?"
input_ids = tokenizer.encode(input_text, return_tensors="pt").to(model.device)
output_ids = model.generate(input_ids, max_length=50)
response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("Response:", response)