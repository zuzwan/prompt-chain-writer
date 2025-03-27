from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env if running locally
load_dotenv()

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = True

# Set up OpenAI client (v1.x SDK)
client = OpenAI()
model_version = "gpt-4-0125-preview"

# Define the system prompt
system_prompt = """You are an expert writer trained in recursive essay composition. Each prompt you receive will be a continuation of a longer essay and must logically connect to the prior section while maintaining clarity and cohesion throughout. Use essay format only. Avoid bullet points, bold formatting, or lists. Use titles and subtitles where appropriate. Write in a style similar to the 'style explainer'."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    prompts = data.get("prompts", [])

    outputs = []
    prior_output = ""
    for i, prompt in enumerate(prompts):
        # Structure the user prompt for clear chaining
        user_prompt = (
            f"You are writing Section {i+1} of a multi-part essay. "
            f"This section must follow logically and stylistically from the prior section.\n\n"
            f"--- PRIOR SECTION ---\n{prior_output}\n\n"
            f"--- INSTRUCTIONS FOR SECTION {i+1} ---\n{prompt}\n\n"
            f"Now write the full draft of Section {i+1}."
        )

        try:
            response = client.chat.completions.create(
                model=model_version,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            output = response.choices[0].message.content
            outputs.append(output)
            prior_output = output
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({"output": f"Error: {str(e)}"})

    # Combine all section outputs into one essay
    full_output = "\n\n".join(outputs)
    return jsonify({"output": full_output})

# Render-compatible app run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)