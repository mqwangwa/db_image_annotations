"""
Fills in the template HTML file.
"""

import json

def fill(results_filepath, output_filepath):
    """
    results_filename: filename of the .json file that contains the results (include .json at end)
    output_filename: filename of the .html file that will be generated (include .html at end)
    """

    with open(results_filepath, "r") as cf:
        data = json.load(cf)

    with open("roads/template.html", "r") as rf:
        html = rf.read()
        newhtml = html.replace("\"{{ placeholder }}\"", json.dumps(data))

        with open(output_filepath, "w") as wf:
            wf.write(newhtml)