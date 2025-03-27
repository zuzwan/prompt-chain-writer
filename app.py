
from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Use gpt-4-0125-preview or latest stable
model_version = "gpt-4-0125-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        user_prompt = f"Section {i+1}: {prompt}\n\nPrevious Section Output (if any):\n{prior_output}"
        try:
            response = openai.ChatCompletion.create(
                model=model_version,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            output = response["choices"][0]["message"]["content"]
            outputs.append(output)
            prior_output = output
        except Exception as e:
            return jsonify({"output": f"Error: {str(e)}"})

    full_output = "\n\n".join(outputs)
    return jsonify({"output": full_output})

if __name__ == "__main__":
    app.run(debug=True)
