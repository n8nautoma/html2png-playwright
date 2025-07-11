from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Server is running"

@app.route('/render', methods=['POST'])

def render():
    html = request.json.get("html", "")
    width = request.json.get("width", 1080)
    height = request.json.get("height", 1350)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_viewport_size({"width": width, "height": height})
            page.set_content(html)
            page.screenshot(path=tmpfile.name)
            browser.close()
        return send_file(tmpfile.name, mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
