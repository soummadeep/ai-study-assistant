import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)
client = genai.Client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash-lite"]
last_error = ""
for model_name in models_to_try:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        last_error = str(e)
        if "503" in last_error or "UNAVAILABLE" in last_error:
            continue
        return jsonify({"error": f"Gemini API Error: {last_error}"}), 500
return jsonify({"error": f"All models temporarily busy: {last_error}"}), 503
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
