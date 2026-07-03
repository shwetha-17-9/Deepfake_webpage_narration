def preprocess_text(input_text):
    # Convert each character to its ASCII value
    processed = [ord(char) for char in input_text]

    # Ensure the length matches the model's expected input size (e.g., 10)
    expected_length = 10  # Adjust this based on your model's input size
    if len(processed) < expected_length:
        # Pad with zeros if the length is too short
        processed += [0] * (expected_length - len(processed))
    elif len(processed) > expected_length:
        # Truncate the list if the length is too long
        processed = processed[:expected_length]
    
    return processed
