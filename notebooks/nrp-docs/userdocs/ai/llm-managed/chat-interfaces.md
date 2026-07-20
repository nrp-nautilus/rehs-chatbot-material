# Chat Interfaces

Source: https://nrp.ai/documentation/userdocs/ai/llm-managed/chat-interfaces

# Chat Interfaces

The NRP hosts several chat interfaces you can use to interact with the managed LLMs without writing any code.

## Open WebUI

If you are looking to chat with an LLM model similar to the interface provided by ChatGPT , we provide the NRP Open WebUI , based on the Open WebUI project. This is a feature-filled chat interface for all of the NRP-hosted models. You can use it to chat with or test out the models.

Visit the NRP Open WebUI interface

On MacOS and Safari you can make it always available in Dock for quick access: having Open WebUI open in Safari, click File → Add to Dock .

## Cherry Studio

You can install the standalone Cherry Studio desktop application.

Visit the Cherry Studio application website

Go to Settings → Model Provider → press the Add button (set Provider Name to NRP or anything else you want, and Provider Type to OpenAI ) → add API Key and API Host ( https://ellm.nrp-nautilus.io/v1 ) → press Fetch model list → press the Add models to the list button at the right of the search box to add all models.

For setting the extra_body JSON parameter, go to Assistants → select an assistant (such as Default Assistant ) → click ⋮ and Edit Assistant → Model Settings → Custom Parameters → Add Parameter → Set Parameter to extra_body , select JSON , and input the JSON contents in the textarea right below (such as {"cache_salt": "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXphYmNkZWZnaGlqa2xtbm9wcQ==", "chat_template_kwargs": {"enable_thinking": true, "thinking": true, "reasoning": {"enabled": true}}} ).

Please do not set Max Tokens (unless you know what you are doing; read the API Access section).

## Chatbox

You can install the standalone Chatbox desktop application or use the web interface version.

Visit the Chatbox application website

Generate the Chatbox configuration in the LLM token generation page . Copy the generated configuration to clipboard — it will already have your personal token.

In Chatbox, go to Settings → Model Provider , scroll down to the end of providers list, and click Import from clipboard .

Please leave Max Output Tokens empty (fill in only Context Window unless you know what you are doing; read the API Access section).
