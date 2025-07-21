from flask import Flask, request, send_file, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ HTML → PNG server is running"

@app.route('/render', methods=['POST'])
def render():
    html = request.json.get("html", "")
    width = request.json.get("width", 1080)
    height = request.json.get("height", 1350)

    if not html:
        return jsonify({"error": "HTML content is missing"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
                )
                page = context.new_page()

                # Установка HTML с ожиданием загрузки сетевых ресурсов
                page.set_content(html, wait_until="networkidle", timeout=60000)

                # Скриншот всей страницы
                page.screenshot(path=tmpfile.name)

                browser.close()

            return send_file(tmpfile.name, mimetype='image/png')

    except PlaywrightTimeoutError:
        return jsonify({"error": "❌ Timeout while rendering page"}), 504

    except Exception as e:
        return jsonify({"error": f"❌ Internal error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
