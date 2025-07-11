from flask import Flask, request, send_file
from playwright.sync_api import sync_playwright
import tempfile

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=8000)
