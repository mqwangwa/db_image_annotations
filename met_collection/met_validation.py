import csv
import pandas as pd

ATTRIBUTES = ["Classification", "Culture", "Medium", "Period"]
correct = [0 for _ in ATTRIBUTES]
incorrect = [0 for _ in ATTRIBUTES]
LEN_ATTRIBUTES = 5

df_labeled = pd.read_excel("FilteredObjects.xlsx")
df_labeled = df_labeled.set_index("Object ID")
labeled_objects = df_labeled.to_dict("index")

df_gemini = pd.read_excel("results.xlsx")
df_gemini = df_gemini.set_index("Object ID")
gemini_objects = df_gemini.to_dict("index")

misclassifications = {}

for object_id, object_attributes in gemini_objects.items():
    labeled_attributes = labeled_objects[object_id]
    for i, attr in enumerate(ATTRIBUTES):
        if object_attributes[attr] == labeled_attributes[attr]:
            correct[i] += 1
        else:
            incorrect[i] += 1
            correct_label = labeled_attributes[attr]
            incorrect_label = object_attributes[attr]
            attr_correct = f"{attr}_{correct_label}"
            if attr_correct not in misclassifications:
                misclassifications[attr_correct] = {}
            misclassifications[attr_correct][incorrect_label] = misclassifications[attr_correct].get(incorrect_label, 0) + 1

print(correct)
print(incorrect)
print(misclassifications)


