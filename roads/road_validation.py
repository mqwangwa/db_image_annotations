# this file validates the computer annotations against a labeled dataset
import csv

ATTRIBUTES = ["tree", "crosswalk", "stop_sign", "traffic_light",
              "chinese_calligraphy", "bike_lane", "fire_hydrant", "sidewalk"]
LEN_ATTRIBUTES = 8

true_positive = [0 for _ in ATTRIBUTES]
true_negative = [0 for _ in ATTRIBUTES]
false_positive = [0 for _ in ATTRIBUTES]
false_negative = [0 for _ in ATTRIBUTES]


class RoadImage:
    def __init__(self, node_id, attributes_present):
        self.id = node_id
        self.attributes_present = attributes_present
        if len(attributes_present) != 8:
            print(f"Error with {self.id} and {attributes_present}")

    def equal(self, other_road_image):
        equiv = True
        assert (self.id == other_road_image.id)
        for i, human_present in enumerate(self.attributes_present):
            gemini_present = other_road_image.attributes_present[i]
            if human_present:
                if gemini_present:
                    true_positive[i] += 1
                else:
                    false_negative[i] += 1
                    equiv = False
            else:
                if gemini_present:
                    false_positive[i] += 1
                    equiv = False
                else:
                    true_negative[i] += 1
        return equiv


labeled_roads = {}
gemini_roads = {}

with open("datasets/gemini_labeled_roads.csv", "r") as f:
    reader = csv.reader(f)
    for line in reader:
        attributes = [value == "True" for value in line[:LEN_ATTRIBUTES]]
        id = int(line[LEN_ATTRIBUTES])
        gemini_roads[id] = RoadImage(id, attributes)

with open("datasets/human_labeled_roads.csv", "r") as f:
    reader = csv.reader(f)
    for line in reader:
        attributes = [value == "1" for value in line[:LEN_ATTRIBUTES]]
        id = int(line[LEN_ATTRIBUTES])
        labeled_roads[id] = RoadImage(id, attributes)

diff = 0
for id, image in labeled_roads.items():
    if not image.equal(gemini_roads[id]):
        diff += 1

print(f"true positive {true_positive}")
print(f"true negative {true_negative}")
print(f"false positive {false_positive}")
print(f"false negative {false_negative}")

# print five digits so that we can report to the hundredth page accurately
# i know there are more intelligent ways to do this
print(f"true positive {[int(100000*val/145) for val in true_positive]}")
print(f"true negative {[int(100000*val/145) for val in true_negative]}")
print(f"false positive {[int(100000*val/145) for val in false_positive]}")
print(f"false negative {[int(100000*val/145) for val in false_negative]}")

print(f"{diff} images different out of {len(labeled_roads)}")
