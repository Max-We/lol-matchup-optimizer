"""
Convert the matrix of all counter scores to one csv file which can be imported into Excel.
"""
import json
import pickle
import csv

from champs import top_champs

with open('full_result.pickle', 'rb') as f:
    data = pickle.load(f)

json_data = json.dumps(data, indent=4)
print(json_data)

with open("output.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=top_champs)
    writer.writeheader()

    for key, values in data.items():
        row = {field: values.get(field, 0) for field in top_champs}
        writer.writerow(row)
