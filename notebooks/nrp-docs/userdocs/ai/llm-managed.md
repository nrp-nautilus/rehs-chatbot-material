# NRP-Managed LLMs

Source: https://nrp.ai/documentation/userdocs/ai/llm-managed

# NRP-Managed LLMs

The NRP hosts a rotating catalog of open-weights LLMs, accessible either through hosted chat interfaces in the browser or programmatically via an OpenAI-compatible API . Models are added and retired as the open-weights frontier moves.

## Pick a model

Every active model is compared side-by-side in the feature matrix, and each has a card with strengths, trade-offs, and recommended uses. A few quick recommendations:

- Frontier reasoning, longest context, multimodal — qwen3

- Agentic coding — kimi , glm-5 , or minimax-m2

- Multimodal with audio (ASR, speech-to-text) — gemma-small

- Reproducible research / general-purpose LTS — gpt-oss

- Embeddings for vector search — qwen3-embedding

## Use the LLMs

For browser chat, the NRP Open WebUI is the most full-featured option. The same OpenAI-compatible API works with desktop apps like Cherry Studio and Chatbox.

For programmatic API access , the OpenAI-compatible endpoint at https://ellm.nrp-nautilus.io/v1 works with the OpenAI Python client, curl , or any compatible library. The API access page also covers cache_salt — recommended for any tenant where prompts shouldn’t be cached across users.

For coding CLIs, ready-to-paste configs are provided for Claude Code , OpenCode , Crush , Kimi CLI , pi , and Copilot CLI .

## Operate responsibly

The NRP applies a Fair Use Policy with per-model concurrency limits — please review it before sending high-volume traffic. SDSC and Internet2 affiliates get higher limits. For real-time capacity and health, the LLM Status page surfaces live Prometheus / vLLM metrics, with one card per Kubernetes container.

## Deploy your own model

If the managed catalog doesn’t fit your need, the NRP supports running your own LLM via vLLM or SGLang. See Managing AI Models for the deployment path.
