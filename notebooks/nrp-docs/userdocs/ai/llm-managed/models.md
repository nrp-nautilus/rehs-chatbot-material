# Available Models

Source: https://nrp.ai/documentation/userdocs/ai/llm-managed/models

# Available Models

A side-by-side comparison of every active NRP-managed LLM, followed by a card per model with strengths, trade-offs, and recommended uses. Click any model name in the matrix to jump to its card; click the HuggingFace link on any card to open the upstream model page.

## Feature Matrix

If your group needs a model marked for active research (so removal is communicated rather than automatic), please reach out via the Nautilus AI/ML channel in Natilus Support . New-model suggestions are also discussed there.

## Generally supported

### qwen3

Qwen/Qwen3.5-397B-A17B-FP8 ↗

Flagship frontier multimodal MoE — Claude/Gemini-level performance, active research model.

Best for: Frontier-quality text and multimodal reasoning · Long-context document and repository analysis · Research workflows requiring reproducibility

#### Strengths

- Frontier-class reasoning and instruction following

- Multimodal (image + video) alongside text

- High-throughput despite large model size

- Sparse MoE keeps per-token compute low despite 397B total parameters

- Official FP8 quantization preserves model quality

- Capacity may be split across multiple GPU pools (A100 + H200) for throughput

#### Trade-offs

- Reasoning mode on by default — adds latency for simple queries

- One of the higher GPU footprint in the catalog

### qwen3-small

Qwen/Qwen3.6-27B ↗

Compact Qwen3.6 — multimodal, agentic, low-latency.

Best for: Latency-sensitive multimodal tasks · Agentic coding and tool use · Long-context tasks where qwen3 is overkill

#### Strengths

- Multimodal (image + video) at a fraction of qwen3's GPU cost

- 262K context window for whole-repo or long-doc work

- Strong agentic and tool-calling behavior

- Lower latency than larger models — good for interactive use

#### Trade-offs

- Lower throughput compared to the model size (dense model)

- Lower reasoning ceiling than the 397B qwen3 on the hardest tasks

- Native bf16 weights use more memory than FP8 (also available officially)

### gpt-oss

openai/gpt-oss-120b ↗

OpenAI's open-weights agentic model — tiny GPU footprint, strong tools, LTS candidate.

Best for: General-purpose chat and assistants · Agentic tool-using workflows · Reproducible research (pinnable model)

#### Strengths

- Runs on a single A100 or two RTX A6000 at full context (MXFP4 + sliding-window attention)

- Strong agentic and tool-calling behavior

- Stable for reproducible research pipelines

- High throughput and low per-token cost optimizes high-concurrency batch use

#### Trade-offs

- Text-only — no vision or video input

- Smaller 128K context compared to Qwen and Kimi models

### gemma

google/gemma-4-31B-it-qat-w4a16-ct ↗

Google's Gemma 4 — multimodal, efficient frontier performance.

Best for: Multimodal tasks (image/video QA, visual analysis) · Efficient general-purpose assistant · Workflows where reasoning is occasional, not constant · Reproducible research (pinnable model)

#### Strengths

- Multimodal (image + video) at a compact 31B size with 4-bit quantization-aware training weights

- Reasoning on by default — disable for faster simple queries

- Solid tool calling support

- Google-quality instruction following

#### Trade-offs

- Lower throughput compared to the model size (dense model)

### qwen3-embedding

Qwen/Qwen3-VL-Embedding-8B ↗

Multimodal embedding model for retrieval and vector search — not a chat model.

Best for: Vector databases and semantic search · RAG pipelines · Multimodal retrieval

#### Strengths

- Embeddings for text, image, and video inputs

- Compatible with Jupyter AI and OpenAI embedding clients

- Compact 8B footprint

#### Trade-offs

- Not a chat model — DO NOT use for chat or completions

## Evaluating

### gemma-small

google/gemma-4-12B-it-qat-w4a16-ct ↗

Tiny Gemma 4 with unique audio input — ASR and speech-to-text on a 12B model.

Best for: Audio transcription and speech-to-text workflows · Lightweight multimodal tasks · Fast, low-cost inference for simple queries

#### Strengths

- Only catalogued model that accepts audio input (ASR, speech-to-text translation)

- Also handles image and video input

- Very small 12B footprint with 4-bit quantization-aware training weights — extremely low latency

- Reasoning on by default — disable for faster simple queries

#### Trade-offs

- Evaluating — availability and config may change

- Lower reasoning and instruction-following ceiling than larger models

### kimi

moonshotai/Kimi-K2.7-Code ↗

Moonshot's 1T-parameter frontier coding model with multimodal inputs.

Best for: Agentic coding (Claude Code, Kimi CLI, Crush) · Large-repo code understanding · Multimodal coding tasks (UI screenshots, diagrams)

#### Strengths

- Frontier-class agentic coding — close to commercial top models on coding benchmarks

- 262K context suits whole-repo analysis

- Multimodal (image + video) for screenshot debugging and design-to-code

- Native Int4 weight keeps memory cost manageable at 1T params

#### Trade-offs

- Evaluating — availability and config may shift

- Largest active-parameter and total-parameter MoE in the catalog; GPU-intensive and slower

- No reasoning toggle (reasoning is implicit in the model behavior)

### glm-5

nvidia/GLM-5.2-NVFP4 ↗

Zhipu's 744B frontier coding model with NVIDIA NVFP4 weights.

Best for: Agentic coding workflows · Long-form reasoning and text tasks · Tool-using agents

#### Strengths

- Strong agentic coding — competitive with commercial frontier models

- NVFP4 quantization preserves quality within limited VRAM

- ~500K context covers large codebases

#### Trade-offs

- Text-only — no multimodal input

- Evaluating — configuration may shift

- Reasoning on by default; adds latency for simple tasks

### minimax-m2

MiniMaxAI/MiniMax-M2.7 ↗

Efficient frontier coding model — 230B in native FP8, fits comfortably on four A100s.

Best for: Cost-efficient or high-throughput agentic coding · Long-context code review and refactoring

#### Strengths

- Frontier-level agentic coding at modest GPU cost

- Native FP8 weights — no quantization quality degradation

- High throughput compared to model size

- ~200K context window for large codebase work

#### Trade-offs

- Text-only — no vision or audio

- No reasoning toggle (reasoning is implicit in the model behavior)
