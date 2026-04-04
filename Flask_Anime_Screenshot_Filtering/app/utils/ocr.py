import easyocr
import re

reader = easyocr.Reader(['en'])

def extract_text(image_path):
    results = reader.readtext(image_path)
    raw_text = [text for (_, text, _) in results]
    return raw_text

def clean_text(raw_text):
    cleaned = []
    for text in raw_text:
        # remove @mentions
        text = re.sub(r'@\w+', '', text)
        # remove emojis
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        # remove pure numbers and timestamps like 1.2K 4:20
        text = re.sub(r'^\d+[\d:KkMm\.]*$', '', text)
        # strip whitespace
        text = text.strip()
        # skip if too short (less than 3 chars)
        if len(text) < 3:
            continue
        cleaned.append(text)
    return cleaned