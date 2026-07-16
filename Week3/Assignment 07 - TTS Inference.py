# Assignment 07 - Hugging Face TTS Inference in Python

import os
import sys

# Step 1 & 2: Import required libraries
try:
    import torch
    from transformers import VitsModel, AutoTokenizer
    import soundfile as sf
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    print("Troubleshooting: Please ensure you are running this script inside the configured virtual environment.")
    sys.exit(1)

def main():
    print("INITIALIZING TEXT-TO-SPEECH (TTS) INFERENCE TASK\n")

    # Step 3: Clone and load the pre-trained TTS model from Hugging Face
    model_id = "facebook/mms-tts-vie"
    print(f"[INFO] Cloning/loading model and tokenizer: {model_id}")
    
    try:
        model = VitsModel.from_pretrained(model_id)
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        print("[INFO] Model loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load model from Hugging Face: {e}")
        sys.exit(1)

    # Step 4: Prepare input text in Vietnamese
    text = "Xin chào anh em đến với bài tập của khoá AI Application Engineer"
    print(f"[INFO] Input Text: '{text}'")

    # Step 5: Tokenize the input text
    print("[INFO] Tokenizing input text...")
    inputs = tokenizer(text, return_tensors="pt")

    # Step 6: Perform inference to generate the waveform
    print("[INFO] Performing forward inference on CPU...")
    try:
        with torch.no_grad():
            output_tensor = model(**inputs).waveform
        
        # VitsModel output waveform shape is usually (1, sequence_length)
        # Convert it to a 1D numpy array for saving with soundfile
        audio_data = output_tensor[0].numpy()
        sampling_rate = model.config.sampling_rate
        print(f"[INFO] Waveform generated. Shape: {output_tensor.shape}, Sampling Rate: {sampling_rate} Hz")
    except Exception as e:
        print(f"[ERROR] Inference failed or errored: {e}")
        sys.exit(1)

    # Step 7: Save audio to file (requires soundfile)
    output_filename = "output.wav"
    print(f"[INFO] Saving synthesized audio to file: {output_filename}")
    try:
        # Save floating point audio data to WAV format
        sf.write(output_filename, audio_data, sampling_rate)
        print(f"SUCCESS: Audio file generated successfully and saved to '{output_filename}'")
    except Exception as e:
        print(f"[ERROR] Failed to write audio file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
