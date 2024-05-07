import re
import joblib

from googletrans import Translator

translator = Translator()


def remove_outliers(text):
    # Define regular expression pattern to match valid characters (letters, numbers, spaces, etc.)
    pattern = r'[\w\s.,?!@#$%^&*()\-+=<>:;"\'{}|\\/]+'

    # Use regular expression to find valid text
    valid_text = re.findall(pattern, text)

    # Join the valid text to form the cleaned text
    cleaned_text = " ".join(valid_text)

    return cleaned_text


def split_text_into_chunks(text, max_chunk_length=1000):
    # List to store text chunks
    chunks = []

    # Initialize variables
    start_index = 0
    end_index = max_chunk_length

    # Iterate until the end of the text
    while start_index < len(text):
        # Find the end index of the current chunk
        if end_index < len(text):
            # Find the nearest word boundary before max_chunk_length
            while end_index > start_index and not text[end_index].isspace():
                end_index -= 1

        # If no space was found before max_chunk_length, return text as is
        if end_index == start_index:
            return text[start_index:]

        # Add the current chunk to the list of chunks
        chunks.append(text[start_index:end_index])

        # Update start_index and end_index for the next chunk
        start_index = end_index
        end_index = min(start_index + max_chunk_length, len(text))

    return chunks


def translate_content(text):
    translated_sentences = []
    cleaned_text = remove_outliers(text)
    chunks = split_text_into_chunks(cleaned_text)
    for i in chunks:
        translated_text = translator.translate(i, dest="en").text
        translated_sentences.append(translated_text)

    return "".join(translated_sentences)


def content_analyzer(data):
    model = joblib.load("model_v2.pkl")
    translated_data = translate_content(data)
    prediction = model.predict([translated_data])
    return prediction[0]
