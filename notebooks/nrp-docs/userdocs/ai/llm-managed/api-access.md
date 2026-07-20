# API Access

Source: https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access

# API Access

To access NRP LLMs through the Envoy AI Gateway , you need to be a member of a group with the LLM flag . Your membership info is on the namespaces page .

Start by creating a token . The token authenticates against an OpenAI-compatible endpoint:

Envoy AI API endpoint

https://ellm.nrp-nautilus.io/v1

You can use this endpoint with curl or any OpenAI-compatible client.

```
curl -H "Authorization: Bearer <your_token>" https://ellm.nrp-nautilus.io/v1/models
```

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://ellm.nrp-nautilus.io/v1",
)

completion = client.chat.completions.create(
    model="gpt-oss",
    messages=[
        {"role": "system", "content": "Talk like a pirate."},
        {"role": "user", "content": "How do I check if a Python object is an instance of a class?"},
    ],
)

print(completion.choices[0].message.content)
```

## Bash + curl

List available models:

```
curl -H "Authorization: Bearer <TOKEN>" https://ellm.nrp-nautilus.io/v1/models
```

Send a chat completion:

```
curl -H "Authorization: Bearer <TOKEN>" -X POST "https://ellm.nrp-nautilus.io/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-oss",
    "messages": [
      {"role": "user", "content": "How do I check if a Python object is an instance of a class?"}
    ]
  }'
```

For pre-built configurations for coding CLIs (OpenCode, Crush, Kimi CLI, Claude Code, Copilot CLI, pi), see Client Configurations .

## Isolating Cached Responses

In your API call, specify a cache_salt key inside extra_body . The value must be a base64-encoded random string of at least 256 bits (43+ characters before encoding) that is known only to you.

```
response = client.chat.completions.create(
    model=model,
    messages=messages,
    extra_body={
        "cache_salt": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXphYmNkZWZnaGlqa2xtbm9wcQ==",
        "chat_template_kwargs": {
          "enable_thinking": True,
          "thinking": True,
          "preserve_thinking": True,
          "clear_thinking": False
        }
    }
)
```

This is supported on vLLM and SGLang models. Without a cache salt, your cached prompts and responses can mix with other users’ caches — which is convenient for shared utility queries but prevents privacy for sensitive prompts and may cause irrelevant cached results to surface in your output.

We would like to apply this automatically per API key but several upstream issues are blocking it: Envoy AI Gateway #1985 , Open WebUI #23012 .
