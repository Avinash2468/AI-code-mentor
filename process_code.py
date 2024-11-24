import sys
import json
from groq import Groq

# Get the code from the command line argument
code = sys.stdin.read()

# Initialize the Groq client
client = Groq(api_key="")

# Create a completion request to the Groq API
completion = client.chat.completions.create(
    model="llama3-groq-70b-8192-tool-use-preview",
    messages=[
        {
            "role": "system",
            "content": (
                "You're a Live AI Code mentor. I want you to understand the code, "
                "identify what we are trying to do and suggest high-level information "
                "around what the code is doing, identify potential issues in the code. "
                "Also, you should suggest tutorials (provide only hyperlinks without any text). "
                "Return the output as a JSON where the key is the section name and the text to be displayed as the value, "
                "which is a list split by sentences. The sections should be as follows in the same order: Potential Issues, "
                "Tutorials, Code Analysis, Suggestions. Make sure the return JSON has the same format even if the code is incomplete."
            )
        },
        {
            "role": "user",
            "content": f"{code}"
        },
    ],
    temperature=0.5,
    max_tokens=1024,
    top_p=0.5,
    stream=True,
    stop=None,
)

# Collect and process the output
output = ""
for chunk in completion:
    content = chunk.choices[0].delta.content or ""
    output += content

# Attempt to extract and validate JSON
try:
    # Find the start and end of the JSON in the output
    start_index = output.find("{")
    end_index = output.rfind("}") + 1

    # Extract the JSON portion
    json_string = output[start_index:end_index]

    # Parse the extracted JSON
    parsed_json = json.loads(json_string)

    # Pretty-print the validated JSON
    print(json.dumps(parsed_json, indent=4))
except json.JSONDecodeError as e:
    print("Error parsing JSON:", e)
    print("Raw output:", output)
