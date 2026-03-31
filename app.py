from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def check_headers(url):
    try:
        r = requests.get(url)
        headers = r.headers

        result = []
        if "X-Frame-Options" not in headers:
            result.append("Missing X-Frame-Options (Clickjacking risk)")
        if "Content-Security-Policy" not in headers:
            result.append("Missing CSP (XSS risk)")
        if "X-XSS-Protection" not in headers:
            result.append("Missing XSS Protection")

        return result if result else ["No major issues found"]
    except:
        return ["Error scanning target"]

@app.route("/", methods=["GET", "POST"])
def home():
    result = []
    if request.method == "POST":
        url = request.form["url"]
        result = check_headers(url)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
