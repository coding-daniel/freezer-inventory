from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route for the web UI
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to receive barcode data
@app.route("/api/scan", methods=["POST"])
def scan_barcode():
    data = request.get_json()
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "Missing barcode"}), 400

    # Placeholder logic — will later call real barcode handler
    return jsonify({"barcode": barcode, "name": f"Dummy Product {barcode}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
