from flask import Flask, request, send_file, jsonify
from playwright.sync_api import sync_playwright, TimeoutError
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Server is running"

@app.route('/render', methods=['POST'])
def render():
    try:
        data = request.get_json(force=True)
        html = data.get("html", "")
        width = data.get("width", 1080)
        height = data.get("height", 1350)

        if not html.strip():
            return jsonify({"error": "Empty HTML"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                page.set_viewport_size({"width": width, "height": height})
                page.set_content(html, wait_until="domcontentloaded")  # faster than "load"
                page.screenshot(path=tmpfile.name, full_page=True)

                page.close()
                context.close()
                browser.close()

            return send_file(tmpfile.name, mimetype='image/png')

    except TimeoutError:
        return jsonify({"error": "Rendering timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port, threaded=True)
