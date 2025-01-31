import re

def custom_json_parser(json_string):
    # Remove leading/trailing spaces and newlines
    json_string = json_string.strip()

    # Remove JSON-like brackets
    if json_string.startswith("{") and json_string.endswith("}"):
        json_string = json_string[1:-1].strip()

    parsed_data = {}
    
    # Split by lines and manually parse key-value pairs
    lines = json_string.split("\n")
    for line in lines:
        # Remove leading/trailing spaces
        line = line.strip()
        
        # Extract key and value using regex
        match = re.match(r'"(.+?)":\s*(.+)', line)
        if match:
            key, value = match.groups()

            # Clean value
            value = value.strip().rstrip(",")  # Remove trailing commas
            
            # Handle boolean values
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            # Handle quoted strings
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            parsed_data[key] = value

    return parsed_data

# Example input string
json_string = '''
{
    "boolean_value": true,
    "Title": "Social Media Post About Enjoyable Meal",
    "summary": "The social media post's claim is supported by the image and text. The image shows a partially eaten plate of fried chicken and fries, and  
    the text expresses positive sentiment (\\"This is so good!\\").  Therefore, the summary of the post accurately reflects the content."
}
'''

# Parse the string
parsed_output = custom_json_parser(json_string)

# Print the output
print(parsed_output)