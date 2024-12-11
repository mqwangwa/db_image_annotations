from flask import Flask, render_template, send_file, request, jsonify
import threading
import os

from osm_csv import create_osm_csvs
from streetview import streetview
from gemini import annotate
from transform import transform
from fill import fill

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map/<name>")
def map(name):
    try:
        return render_template(f"{name}.html")
    except:
        return render_template("notfound.html")
    
@app.route("/data/<filename>")
def image(filename):
    return send_file(f"../data/{filename}", mimetype="image/jpg")


def pipeline(name, schema_str):
    osm_filepath = f"roads/intermediate_data/{name}.osm"
    edges_csv_path = f"roads/intermediate_data/{name}_edges.csv"
    nodes_csv_path = f"roads/intermediate_data/{name}_nodes.csv"
    gemini_output_path = f"roads/intermediate_data/{name}_results_gemini.csv"
    results_json_path = f"roads/intermediate_data/{name}_results.json"
    output_html_path = f"roads/templates/{name}.html"

    create_osm_csvs(osm_filepath, edges_csv_path, nodes_csv_path)
    streetview(osm_filepath)
    annotate(schema_str, nodes_csv_path, gemini_output_path)
    transform(nodes_csv_path, gemini_output_path, results_json_path)
    fill(results_json_path, output_html_path)

@app.route("/start", methods=["POST"])
def start():
    name = request.form["name"]
    schema_str = request.form["schema"]

    # save the uploaded file    
    file = request.files["file"]
    file.save(f"roads/intermediate_data/{name}.osm") # assume the user uploaded a .osm file

    thread = threading.Thread(target=pipeline, args=(name, schema_str))
    thread.start()

    out = {"link": f"/map/{name}"}
    return jsonify(out)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, port=5001)