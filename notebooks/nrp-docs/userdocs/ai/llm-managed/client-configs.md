# Client Configurations

Source: https://nrp.ai/documentation/userdocs/ai/llm-managed/client-configs

# Client Configurations

Pre-built configurations for popular coding CLIs. The endpoint and token setup is covered on API Access — start there if you don’t have a token yet.

Use the right-hand “On this page” navigation to jump to your client. Every config below assumes:

- Endpoint: https://ellm.nrp-nautilus.io/v1 (Anthropic-compatible at /anthropic )

- Token: the value from the LLM token page , passed in Authorization: Bearer … or whatever the client’s API-key field expects.

- For cache_salt , this needs to be on the same level as chat_template_kwargs , but not inside. Example: {"cache_salt": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXphYmNkZWZnaGlqa2xtbm9wcQ==", "chat_template_kwargs": {"enable_thinking": true, "thinking": true, "preserve_thinking": true, "clear_thinking": false}}

## VS Code

https://code.visualstudio.com

VS Code can use NRP-managed LLMs through the Chat: Manage Language Models command. This lets you pick NRP models from the model selector in Copilot Chat.

- Open the Command Palette ( Ctrl+Shift+P / Cmd+Shift+P ) and run Chat: Manage Language Models .

- Click Add Models .

- Choose Custom Endpoint .

- Enter your endpoint URL: https://ellm.nrp-nautilus.io/v1/chat/completions

Paste the configuration below when prompted. The apiKey uses VS Code’s ${input:...} substitution, so you’ll be asked for your LLM token the first time you use the model — the token is then stored securely by VS Code.

```
{
  "name": "NRP",
  "vendor": "customendpoint",
  "apiKey": "${input:chat.lm.secret.2630e22e}",
  "apiType": "chat-completions",
  "models": [
    {
      "id": "glm-5",
      "name": "glm-5",
      "url": "https://ellm.nrp-nautilus.io/v1/chat/completions",
      "toolCalling": true,
      "vision": false,
      "maxInputTokens": 524288,
      "maxOutputTokens": 100000
    },
    {
      "id": "qwen3",
      "name": "qwen3",
      "url": "https://ellm.nrp-nautilus.io/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 1010000,
      "maxOutputTokens": 100000
    },
    {
      "id": "kimi",
      "name": "kimi",
      "url": "https://ellm.nrp-nautilus.io/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 262144,
      "maxOutputTokens": 100000
    }
  ]
}
```

## OpenCode

https://github.com/anomalyco/opencode

After applying the configuration below, search for NRP in the list of models ( Ctrl+P → Switch models , and to select a variant, use Ctrl+P → Switch model variant ).

Either set the OPENAI_API_KEY environment variable or replace {env:OPENAI_API_KEY} with the actual API key. Adjust "output" as needed, but never set it close to or larger than "context" .

Contents of ~/.config/opencode/opencode.jsonc (use "enable_thinking" or "thinking" as required by the model):

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "NRP": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "NRP",
      "options": {
        "baseURL": "https://ellm.nrp-nautilus.io/v1",
        "apiKey": "{env:OPENAI_API_KEY}"
      },
      "models": {
        "kimi": {
          "name": "kimi",
          "limit": {
            "context": 262144,
            "output": 32768
          },
          "modalities": {
            "input": ["text", "image", "video"],
            "output": ["text"]
          }
        }
      }
    }
  }
}
```

For changing the "chat_template_kwargs" configuration or setting additional variants (on allowed models), use the below configuration within each model (in the same level as "name" ):

```
          "options": {
            "chat_template_kwargs": {
              "thinking": true,
              "preserve_thinking": true
            }
          },
          "variants": {
            "instruct": {
              "chat_template_kwargs": {
                "thinking": false,
                "preserve_thinking": false
              }
            }
          },
```

## Crush

https://github.com/charmbracelet/crush

After applying the configuration below, search for NRP in the list of models. Adjust "default_max_tokens" as needed; never push it close to or above "context_window" .

See also Andrea Zonca’s writeup: Configure NRP LLM with OpenCode and Crush .

Contents of ~/.config/crush/crush.json (use "enable_thinking" or "thinking" as required by the model):

```
{
  "$schema": "https://charm.land/crush.json",
  "options": {
    "disable_metrics": true,
    "disable_provider_auto_update": false,
    "debug": false,
    "debug_lsp": false,
    "attribution": {
      "trailer_style": "none",
      "generated_with": false
    }
  },
  "mcp": {},
  "providers": {
    "nrp": {
      "name": "NRP",
      "type": "openai-compat",
      "base_url": "https://ellm.nrp-nautilus.io/v1",
      "api_key": "<LLM_API_KEY>",
      "models": [
        {
          "id": "kimi",
          "name": "kimi",
          "context_window": 262144,
          "default_max_tokens": 32768,
          "modalities": {
            "input": ["text", "image", "video"],
            "output": ["text"]
          }
        }
      ]
    }
  }
}
```

For changing the "chat_template_kwargs" configuration or setting additional "extra_body" parameters, use the below configuration within each model (in the same level as "models" ):

```
      "extra_body": {
        "chat_template_kwargs": {
          "thinking": true,
          "preserve_thinking": true
        }
      },
```

## pi

https://pi.dev

Press Ctrl-L to switch models and search for NRP (or type /model modelname ).

apiKey accepts the literal key, an environment variable name ( OPENAI_API_KEY ), or a shell command ( !decrypt_key NRP ).

Contents of ~/.pi/agent/models.json :

```
{
  "providers": {
    "nrp": {
      "baseUrl": "https://ellm.nrp-nautilus.io/v1",
      "api": "openai-completions",
      "apiKey": "<YOUR_API_KEY>",
      "models": [
        {
          "id": "kimi",
          "name": "kimi",
          "input": ["text", "image"],
          "contextWindow": 262144,
          "reasoning": true
        },
        {
          "id": "qwen3-small",
          "name": "qwen3-small",
          "input": ["text", "image"],
          "contextWindow": 262144,
          "reasoning": true,
          "compat": {
            "thinkingFormat": "qwen-chat-template",
            "supportsDeveloperRole": false
          }
        }
      ]
    }
  }
}
```

## Kimi CLI

https://github.com/MoonshotAI/kimi-cli

Contents of ~/.kimi/config.toml :

```
default_model = "kimi"
default_thinking = true
default_yolo = false
default_plan_mode = true
show_thinking_stream = true

[providers.nrp]
type = "openai_legacy"
base_url = "https://ellm.nrp-nautilus.io/v1"
api_key = "<YOUR_API_KEY>"

[models.kimi]
provider = "nrp"
model = "kimi"
max_context_size = 262144
capabilities = ["thinking", "image_in", "video_in"]

[services]
```

## Claude Code

https://github.com/anthropics/claude-code

Claude Code talks to NRP through the Anthropic-compatible endpoint at /anthropic . Set the variables below in your shell or ~/.claude/.env :

```
ANTHROPIC_BASE_URL="https://ellm.nrp-nautilus.io/anthropic"
ANTHROPIC_API_KEY="<llm-token>"
ANTHROPIC_DEFAULT_OPUS_MODEL="<name-of-nrp-model>"
ANTHROPIC_DEFAULT_SONNET_MODEL="<name-of-nrp-model>"
ANTHROPIC_DEFAULT_HAIKU_MODEL="<name-of-nrp-model>"
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY="1"
CLAUDE_CODE_ENABLE_TELEMETRY="0"
API_TIMEOUT_MS="3000000"
DISABLE_TELEMETRY="1"
```

## Copilot CLI

https://github.com/github/copilot-cli

Set COPILOT_PROVIDER_MAX_PROMPT_TOKENS to the model’s context length and COPILOT_PROVIDER_MAX_OUTPUT_TOKENS to a smaller value (roughly 1/16 to 1/4 of the context, depending on the task).

```
COPILOT_PROVIDER_BASE_URL="https://ellm.nrp-nautilus.io/v1"
COPILOT_PROVIDER_KEY="<llm-token>"
COPILOT_MODEL="<name-of-nrp-model>"
COPILOT_PROVIDER_MAX_PROMPT_TOKENS="<context-length>"
COPILOT_PROVIDER_MAX_OUTPUT_TOKENS="<max-output>"
```
