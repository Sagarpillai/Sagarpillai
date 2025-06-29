from flask import Flask, request, jsonify
import google.generativeai as genai
from markdown import markdown

app = Flask(__name__)

# ✅ Configure Gemini with your API key
genai.configure(api_key="AIzaSyB3ccvQqCHh6Y_40OI0SWZjP_p-P0bQDYQ", transport="rest")

# ✅ Initialize the model (you missed this line!)


model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction="You are a helpful shopping assistant. Be concise, and suggest only 3 or 4 products at a time. Reply in simple English.while recommending give the product name its price and link to buy it from according to india. Format responses using Markdown. Use line breaks, numbered lists, and bold product names.if they ask anything other than products tell them ur unfit to answer this. "
)


@app.route('/')
def index():
    return open("index.html", encoding="utf-8").read()

@app.route('/ask', methods=['POST'])
def chat():
    user_msg = request.json['message']
    print("User asked:", user_msg)

    try:
        response = model.generate_content(user_msg)
        print("Gemini replied:", response.text)
        reply_html = markdown(response.text)
        return jsonify({"reply": reply_html})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Sorry, I couldn't process that."})

if __name__ == '__main__':
    app.run(debug=True)
