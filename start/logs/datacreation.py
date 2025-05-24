import json

sample_data = {
    "slot_name": "1",
    "slot_type": "FPORT",
    "shelf_id": "1"
}

# Generate a list with 1000 copies of the sample data
data_list = [sample_data.copy() for _ in range(1000)]

# Save to a JSON file
with open("sample_slots.json", "w") as f:
    json.dump(data_list, f, indent=2)
