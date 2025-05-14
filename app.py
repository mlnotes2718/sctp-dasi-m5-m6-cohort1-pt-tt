from flask import Flask, render_template, request
from google import genai
import markdown
import os

#Load environment variables from .env file
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.environ.get("GOOGLE_API")
#print("API Key:", api_key)  # Debugging line to check if the API key is loaded correctly

api_key = os.getenv('GOOGLE_API')

client = genai.Client(api_key=api_key)

app = Flask(__name__)
model = "gemini-2.0-flash"

@app.route("/",methods=["GET","POST"])
def index():
        return(render_template("index.html"))

@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/gemini_reply",methods=["GET","POST"])
def gemini_reply():
    q = request.form.get("q")
    r = client.models.generate_content(model=model,contents=q)
    r_html = markdown.markdown(
            r.text,
            extensions=["fenced_code", "codehilite"]  
    )
    return(render_template("gemini_reply.html",r=r_html))

if __name__ == "__main__":
    app.run()
