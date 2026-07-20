# Model Lifecycle and Changelog

Source: https://nrp.ai/documentation/userdocs/ai/llm-managed/lifecycle

# Model Lifecycle and Changelog

The NRP catalog rotates quickly to track the open-weights frontier. Newer, faster models replace obsolete ones, and GPU allocations are shifted toward what the community is actually using. This page explains the process and lists what’s changed recently.

## How models are added and removed

Added — new models are added based on benchmarks ( artificialanalysis.ai ) and qualitative evidence (e.g. r/LocalLLaMA ), with the final decision made by administrators in discussion with users.

Removed — obsolete models are removed when smaller models perform better all-around or another model has clearly replaced the use case.

Deprecated — research groups that need a specific model for reproducibility can declare research usage. Deprecated models stay up until the research concludes, but their replacement is still encouraged. If your group depends on a model that has been deprecated or removed, please reach out via the Nautilus AI/ML channel .

GPU allocation is the limiting factor: larger models that require many GPUs are removed sooner if relative performance falls behind, while small or efficient models get more leniency. New-model decisions and retirement discussion happen in the same Matrix channel.

## Recent changes

- glm-5 ( nvidia/GLM-5.1-NVFP4 ) was changed to GLM-5.2 ( nvidia/GLM-5.2-NVFP4 )

- kimi was changed from moonshotai/Kimi-K2.6 to moonshotai/Kimi-K2.7-Code .

- gemma was changed from google/gemma-4-31B-it to google/gemma-4-31B-it-qat-w4a16-ct .

- gemma-small was changed from google/gemma-4-E4B-it to google/gemma-4-12B-it-qat-w4a16-ct . Context size changed.

## Older changes

- glm-4.7 ( zai-org/GLM-4.7-FP8 ) was updated to glm-5 ( nvidia/GLM-5.1-NVFP4 )

- olmo ( allenai/Olmo-3.1-32B-Instruct ) has been removed due to lack of usage.

- gemma3 was renamed to gemma and switched from google/gemma-3-27b-it to google/gemma-4-31B-it . Context size changed.

- qwen3-small switched from Qwen/Qwen3.5-27B to Qwen/Qwen3.6-27B ; context size changed.

- gemma-small ( google/gemma-4-E4B-it ) was added with audio input support.

- minimax-m2 upgraded from MiniMax-M2.5 to MiniMax-M2.7 .

- kimi upgraded from Kimi-K2.5 to Kimi-K2.6 .

- qwen3-embedding ( Qwen/Qwen3-VL-Embedding-8B ) added on the AI Gateway.

- embed-mistral ( intfloat/e5-mistral-7b-instruct ) decommissioned and replaced with qwen3-embedding due to incompatibilities with Jupyter AI.

- llama3-sdsc ( Llama-3.3-70B-Instruct ) removed from the Envoy AI Gateway after a long deprecation.

- glm-v (GLM-4.6V multimodal route) removed from the Envoy AI Gateway. Use glm-4.7 for text and other multimodal options for vision/video.

- minimax-m2 changed from MiniMaxAI/MiniMax-M2.1 to MiniMaxAI/MiniMax-M2.5 .

- qwen3 changed from Qwen3-VL-235B-A22B-Thinking-FP8 to Qwen3.5-397B-A17B-FP8 .

Added/Changed

- glm-4.7 switched to the official zai-org/GLM-4.7-FP8 ; more GPUs allocated due to its position in the catalog.

- kimi switched to the multimodal moonshotai/Kimi-K2.5 .

Removed

- olmo ( allenai/OLMo-2-0325-32B-Instruct ) and gorilla ( gorilla-llm/gorilla-openfunctions-v2 ) removed — both had been broken for months without anyone reporting.

- glm-v upgraded to zai-org/GLM-4.6V-FP8 — larger context size.

- glm-4.6 renamed to glm-4.7 and changed to the QuantTrio/GLM-4.7-GPTQ-Int4-Int8Mix quant.

- minimax-m2 changed from MiniMaxAI/MiniMax-M2 to MiniMaxAI/MiniMax-M2.1 .

Added/Changed

- qwen3 changed to Qwen3-VL-235B-A22B-Thinking-FP8 — adds state-of-the-art vision and video.

- kimi ( moonshotai/Kimi-K2-Thinking ) — frontier programming model comparable to Claude Sonnet 4.5 / GPT-5.

- glm-4.6 ( QuantTrio/GLM-4.6-GPTQ-Int4-Int8Mix ) — comparable to Claude Sonnet 4 / Gemini 2.5 Pro.

- minimax-m2 ( MiniMaxAI/MiniMax-M2 ) — comparable to Sonnet 4 / Gemini 2.5 Pro, fits in four A100s.

- gpt-oss ( openai/gpt-oss-120b ) — capable agentic model on a single A100 or two RTX A6000 GPUs. LTS candidate, supersedes deprecated Llama3 models.

- gemma3 moved to 2× RTX A6000 GPUs. Sliding-window attention allows full context.

- glm-v switched to zai-org/GLM-4.5V-FP8 on 4× L40 GPUs.

Removed

- llama3 ( meta-llama/Llama-3.2-90B-Vision-Instruct ) — consumed 4 A100s while being outperformed by single-GPU models.

- deepseek-r1 — used 8 GPUs but was very slow (5–6 tokens/s) at larger contexts.

- watt ( watt-ai/watt-tool-8B ) — removed for inactivity.
