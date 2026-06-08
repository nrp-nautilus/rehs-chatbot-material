# Python Cheatsheet

The Python you'll actually use this summer. Bookmark and keep open.

---

## Strings

```python
name = "Alice"
greeting = f"Hello, {name}!"        # f-string (your friend)
greeting.upper()                    # "HELLO, ALICE!"
greeting.split(",")                 # ['Hello', ' Alice!']
"-".join(["a", "b", "c"])           # "a-b-c"
"  hi  ".strip()                    # "hi"
"hello".replace("l", "L")           # "heLLo"
"abc"[0]                            # "a"
"abc"[-1]                           # "c"
"abc"[1:]                           # "bc"
```

## Numbers & math

```python
3 + 4              # 7
10 / 3             # 3.333...   (always float in Python 3)
10 // 3            # 3          (integer division)
10 % 3             # 1          (remainder)
2 ** 8             # 256        (power)
int("42")          # 42
float("3.14")      # 3.14
round(3.7)         # 4
```

## Lists

```python
nums = [1, 2, 3]
nums.append(4)             # [1, 2, 3, 4]
nums[0]                    # 1
nums[-1]                   # 4
nums[1:3]                  # [2, 3]
len(nums)                  # 4
4 in nums                  # True

# Loop
for n in nums:
    print(n)

# List comprehension (powerful!)
squares = [n*n for n in nums]               # [1, 4, 9, 16]
evens   = [n for n in nums if n % 2 == 0]   # [2, 4]
```

## Dictionaries

```python
person = {"name": "Alice", "age": 17}
person["name"]                  # "Alice"
person["email"] = "a@b.com"     # add a key
person.get("phone", "n/a")      # "n/a" if missing
"name" in person                # True

# Loop
for key, value in person.items():
    print(f"{key}: {value}")
```

## Booleans & conditions

```python
True, False
not True              # False
True and False        # False
True or False         # True

x = 5
if x > 10:
    print("big")
elif x > 0:
    print("small")
else:
    print("zero or negative")
```

## Loops

```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 2):  # 2, 4, 6, 8
    print(i)

count = 0
while count < 3:
    print(count)
    count += 1

# Skip + stop
for i in range(10):
    if i == 3: continue   # skip 3
    if i == 7: break      # stop at 7
    print(i)
```

## Functions

```python
def greet(name, greeting="Hello"):    # default arg
    return f"{greeting}, {name}!"

greet("Alice")                # "Hello, Alice!"
greet("Bob", greeting="Hi")   # "Hi, Bob!"

# Type hints (you should use these)
def add(a: int, b: int) -> int:
    return a + b
```

## Files

```python
# Read
with open("notes.txt") as f:
    content = f.read()           # whole file as string
    # or:
    for line in f:
        print(line.rstrip())     # line by line

# Write
with open("out.txt", "w") as f:
    f.write("hello\n")

# JSON
import json
data = {"name": "Alice", "age": 17}
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
with open("data.json") as f:
    loaded = json.load(f)
```

## Error handling

```python
try:
    risky_thing()
except FileNotFoundError as e:
    print(f"File missing: {e}")
except Exception as e:
    print(f"Something else broke: {e}")
finally:
    print("This always runs")
```

## Imports

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

# Your own modules
from src.embed.search import search
```

## Virtual environments (use these!)

```bash
# Create a venv in your project
python3 -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate

# Install stuff
pip install openai streamlit chromadb

# Save what's installed
pip freeze > requirements.txt

# Install from a file
pip install -r requirements.txt

# Leave the venv
deactivate
```

## Environment variables (.env files)

```python
# .env file (NEVER commit this)
NRP_LLM_TOKEN=sk-xxxxxxxxxx
NRP_LLM_BASE_URL=https://ellm.nrp-nautilus.io/v1
```

```python
# In your Python
import os
from dotenv import load_dotenv
load_dotenv()                            # reads .env into os.environ
token = os.environ["NRP_LLM_TOKEN"]      # raises if missing
url = os.environ.get("NRP_LLM_BASE_URL", "default-url")
```

## The OpenAI client (NRP-compatible)

```python
from openai import OpenAI

client = OpenAI(api_key=..., base_url="https://ellm.nrp-nautilus.io/v1")

# Chat
r = client.chat.completions.create(
    model="gpt-oss",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
    ],
    temperature=0.7,
    stream=False,
)
print(r.choices[0].message.content)
print(r.usage.total_tokens)

# Streaming
for chunk in client.chat.completions.create(model="gpt-oss", messages=[...], stream=True):
    print(chunk.choices[0].delta.content or "", end="")

# Embeddings
e = client.embeddings.create(model="qwen3-embedding", input=["text"])
vec = e.data[0].embedding
```

## Streamlit (the 5 things you need)

```python
import streamlit as st

st.title("My App")
st.write("Hello world")

name = st.text_input("Your name")
if st.button("Say hi"):
    st.write(f"Hi, {name}!")

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
if prompt := st.chat_input("Type here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
```

Run with: `streamlit run app.py`

---

## Style tips

- **Snake_case** for variables and functions: `my_variable`, not `myVariable`.
- **CONSTANT_CASE** for module-level constants: `MAX_TOKENS = 1024`.
- **Type hints** make code easier to read: `def f(x: int) -> str:`
- **f-strings** beat `"%s" % x` and `"{}".format(x)`. Use them.
- **`with open(...)`** beats manual `f = open(); ...; f.close()`. The `with` closes for you.

---

## Anti-patterns to avoid

```python
# ❌ catching every exception silently
try:
    do_stuff()
except:           # catches Ctrl+C too! never do this
    pass

# ✅ catch what you expect
try:
    do_stuff()
except FileNotFoundError as e:
    handle(e)

# ❌ mutable default args
def add_item(item, items=[]):       # the [] is *shared across calls*!
    items.append(item)
    return items

# ✅ use None
def add_item(item, items=None):
    items = items or []
    items.append(item)
    return items
```
