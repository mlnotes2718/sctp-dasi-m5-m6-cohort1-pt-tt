from flask import Flask, render_template, request
from google import genai
import openai
import markdown
import os

#Load environment variables from .env file
# from dotenv import load_dotenv
# load_dotenv()
# genmini_api_key = os.environ.get("GOOGLE_API")
# openai_api_key = os.environ.get("OPENAI_API")
#print("API Key:", api_key)  # Debugging line to check if the API key is loaded correctly

genmini_api_key = os.getenv('GOOGLE_API')
openai_api_key = os.getenv('OPENAI_API')

genmini_client = genai.Client(api_key=genmini_api_key)
genmini_model = "gemini-2.0-flash"

openai_client = openai.OpenAI(api_key=openai_api_key)
openai_model = "gpt-4o"


app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def index():
        return(render_template("index.html"))

@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/gemini_reply",methods=["GET","POST"])
def gemini_reply():
    q = request.form.get("q")
    r = genmini_client.models.generate_content(model=genmini_model,contents=q)
    r_html = markdown.markdown(
            r.text,
            extensions=["fenced_code", "codehilite"]  
    )
    return(render_template("gemini_reply.html",r=r_html))

@app.route("/openai",methods=["GET","POST"])
def openai():
    return(render_template("openai.html"))


@app.route("/openai_reply",methods=["GET","POST"])
def openai_reply():
    q = request.form.get("q")
    r = openai_client.chat.completions.create(model=openai_model,messages=[{"role": "user", "content": q}],)
    r_html = markdown.markdown(
            r.choices[0].message.content,
            extensions=["fenced_code", "codehilite"]  
    )
    return(render_template("openai_reply.html",r=r_html))

if __name__ == "__main__":
    app.run()
