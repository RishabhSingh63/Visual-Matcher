from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import io, os, json, math

BASE_DIR = os.path.dirname(__file__)
PRODUCTS_DIR = os.path.join(BASE_DIR, "products")
with open(os.path.join(PRODUCTS_DIR, "metadata.json")) as f:
    METADATA = json.load(f)

def avg_color_of_image(image):
    # image: PIL Image
    small = image.resize((1,1))
    return tuple(small.getpixel((0,0)))

def color_distance(a,b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")

@app.route("/api/search", methods=["POST"])
def search():
    # Accepts form-data 'image' file OR JSON with 'image_url' (URL fetching disabled offline)
    if "image" in request.files:
        file = request.files["image"]
        try:
            img = Image.open(file.stream).convert("RGB")
        except Exception as e:
            return jsonify({"error":"Invalid image"}), 400
    else:
        data = request.get_json() or {}
        image_url = data.get("image_url")
        if image_url:
            return jsonify({"error":"URL search not available in this offline demo. Please upload an image file."}), 400
        return jsonify({"error":"No image uploaded"}), 400

    q_color = avg_color_of_image(img)
    # compute distances to products
    results = []
    for p in METADATA:
        dist = color_distance(q_color, tuple(p["avg_color"]))
        results.append({"id":p["id"], "name":p["name"], "category":p["category"],
                        "image": p["image"], "score": float(dist)})
    # smaller distance = more similar; sort ascending
    results = sorted(results, key=lambda x: x["score"])[:10]
    # normalize similarity score to 0-100
    maxd = max(r["score"] for r in results) if results else 1
    for r in results:
        r["similarity"] = round(100*(1 - r["score"]/ (maxd+1e-6)),2)
    return jsonify({"query_avg_color": q_color, "results": results})

# Serve product images
@app.route("/products/<path:filename>")
def product_image(filename):
    return send_from_directory(os.path.join(BASE_DIR, "products"), filename)

# Serve frontend static build if exists
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, "index.html")
    return "Backend is running. Frontend build not found.", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)