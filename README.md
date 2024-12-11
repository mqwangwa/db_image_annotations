# Data Annotation on Specialized Image Collections

This repo contains all the code for the final project in 6.5830 by Margaret Wang and Zi Yan Wu. It is composed of three folders, `roads` for the first case study we performed, `met_collection` for the second case study, and `archive_ignore` which contains old code from other experiments.

## Case Study Code Organization

For both case studies, we followed the same four steps.
1. Collect an image dataset of interest
2. Define a schema for that dataset
3. Send each image and the schema to Gemini. Aggregate the returned annotations to build an annotated dataset.
4. Validate the annotated dataset against a human-labeled sample.

The code for the two case studies are presented as examples. We would expect a user to perform steps 1 and 2, and our system handles step 3 to build the annotated dataset. Step 4 is optional for the user, but it was needed for evaluating our system.

We describe the codebase for the Met Collection case study below, and the structure for `roads` is extremely similar. However, that folder contains additional code for collecting the data from OpenStreetMaps and building the visualization.

## Roads
### 01. Setup
* The required packages for this can be found in ```requirements.txt``` and can be installed through ```pip install -r requirements.txt```
* Next, you have to populate the values in the ```.env``` file with your API keys for each respective service. You will need an API key for Google's Street View and Gemini services
* And lastly, you will have to go on OpenStreetMaps to select a location and download its corresponding ```.osm``` file

### 02. Running the Tool
Within the main directory, run ```python3 roads/web.py``` to start up the web server, which will be where you mainly interact with this tool. Head to ```127.0.0.1:5001``` on your browser to access the main page.

On this page, you will want to fill out the information on the form. The name field is for naming your current run of the tool. The schema field should be in JSON format with the query being keys and the data type being the values. For this tool, only "bool" is accepted as a value. The following is an example of an accepted schema value:
~~~
{
  "tree": "bool",
  "stop_sign": "bool",
  "crosswalk": "bool",
  "traffic_light": "bool"
}
~~~
And in the last field, upload your ```.osm``` file for the location you want to search at. 

Pressing the "Start" button will then start the visualization process. A link will appear where your results will be located at after everything has finished. (Note: Due to Gemini's free tier rate limits, only a max of 1,500 nodes can be processed per day and only up to 15 requests per minute can be sent, so depending on how big your location is, this step could take more than an hour).

### 03. Results

Once the tool has completed all the steps, you can simply load (or reload) the link generated and you should see a map. You can then press on the toggles above for your query attributes to see all the different markers and the corresponding street image that contain that query.

## Met Collection
### 01. Building the Image Dataset
We obtained images from the Metropolitan Museum of Art [Open Access Catalog](https://github.com/metmuseum/openaccess). This provided both high-resolution images of their catalog in `MetObjects.xlsx` and an extensive catalog of the objects in their collection. While this file is too large to store in our repo, it can be downloaded directly from their [repo](https://github.com/metmuseum/openaccess) and is also available in our [Google Drive](https://docs.google.com/spreadsheets/d/1iwkoUX1Paw825pMlYPMSZD9jXkgRi4va/edit?usp=drive_link&ouid=102195568975902391941&rtpof=true&sd=true). \
In `public_domain_01.py`, we filtered the catalog to only select objects available in the public domain and that were in the top 20 categories for the Period, Classification, Culture, and Medium fields. Using these filters, we created a labeled dataset of object IDs and the features associated with each object. This is in `FilteredObjects.xlsx` which is in our repo under `met_collection/datasets/`. Notably, we did not download the image dataset locally, instead storing only the object ID, which is different from the roads case study.
### 02. Defining the Schema
Based on the categories present in `FilteredObjects.xlsx`, we constructed a schema where each field was an enum. See an example in `schema_met_02.py`.
### 03. Annotating the Dataset
Due to rate limits, we randomly sampled 1% of the dataset for annotation. To annotate the dataset, we perform two steps for each object ID. First, we make a request to the Met Museum's [API](https://metmuseum.github.io/) to obtain the URL where the image is hosted. Second, we send both the image and the schema defined in Step 2 to Gemini, and we receive an annotated response. These responses are combined to form `GeminiResults.xlsx`.
### 04. Validating the Annotations
We validate against the Met's own labeling from their catalog. Using the filtered columns in `FilteredObjects.xlsx`, we compare the Gemini labels with the human labels and output the total number of correct and incorrect categorizations for each feature. We also output a dictionary to represent the miscategorizations, mapping each correct label to what it was incorrectly classified as and the frequency of the mistake.
