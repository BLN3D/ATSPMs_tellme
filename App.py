import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# Security: Uses Environment Variable for the API Key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    img = Image.open(file.stream)
    
    prompt = """
    Analyze this Purdue Coordination Diagram (PCD).
    Provide the following in JSON format:
    1. 'aog': Estimated Arrivals on Green percentage.
    2. 'pr': Estimated Platoon Ratio.
    3. 'los': Inferred Level of Service (A-F).
    4. 'summary': A 2-sentence engineering summary of the coordination quality.
    """

    try:
        response = model.generate_content([prompt, img])
        # Extracting clean JSON from the AI response
        json_res = response.text.replace('```json', '').replace('```', '').strip()
        return json_res
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
