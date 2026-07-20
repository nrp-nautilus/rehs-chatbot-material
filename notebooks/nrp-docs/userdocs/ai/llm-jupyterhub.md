# LLM in JupyterHub

Source: https://nrp.ai/documentation/userdocs/ai/llm-jupyterhub

# LLM in JupyterHub

You can easily experiment with LLMs in JupyterHub. We provide the managed one , or you can run your own .

Make sure your /home/jovyan volume is large enough to hold the LLM model (which usually reaches hundreds of GB), and ask admins to extend it if nesessary.

Run a Jupyter pod with enough memory and cores for your model and appropriate GPU type.

Install the Hugging Face interface:

!pip install --user --upgrade diffusers accelerate transformers

Then run Stable Diffusion in python to generate an image:

```
from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "An astronaut riding a horse, painting in Dali style"
image = pipe(prompt).images[0]

image.save("astronaut_rides_horse.png")
```

Or do text generation:

```
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")

prompt = "Hey, are you conscious? Can you talk to me?"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=30)
tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
```

Each model comes with documentation on how to use one.

The model files will be cached in /home/jovyan/.cache/huggingface folder.
