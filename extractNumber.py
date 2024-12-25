import re

def extract_number(string):
    pattern1 = r'\d+\.?\d*K'  # Regular expression pattern to match one or more digits
    pattern2 = r'\d+'  # Regular expression pattern to match one or more digits

    # Use re.findall() to find all occurrences of the pattern in the string
    matches1 = re.findall(pattern1, string)
    matches2 = re.findall(pattern2, string)

    if matches1:
        # The first element in the matches list will be the extracted numbe
        extracted_number = matches1[0]
    elif matches2:
        extracted_number = matches2[0]
    else:
        extracted_number = "None"
    return extracted_number

