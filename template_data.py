import json

# Sample JSON data for pre-designed HTML templates
template_data = []


def load_templates(filename="templates.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return template_data  # Fall back to the default template data
