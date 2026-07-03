import torch
from g2p_en import G2p
from scipy.io.wavfile import write

# Define the VocoderModel
class VocoderModel(torch.nn.Module):
    def __init__(self):
        super(VocoderModel, self).__init__()-
        # Adjust this to match your model's expected input/output
        self.fc1 = torch.nn.Linear(1000, 512)  # First Linear layer
        self.fc2 = torch.nn.Linear(512, 256)  # Second Linear layer
        self.fc3 = torch.nn.Linear(256, 22050)  # Output layer for audio waveform

    def forward(self, x):
        print(f"Input to model: {x.shape}")  # Debug input shape
        x = torch.relu(self.fc1(x))  # Apply ReLU activation
        x = torch.relu(self.fc2(x))  # Apply ReLU activation
        x = self.fc3(x)  # Final output layer
        return x

    def infer(self, mel_spectrogram):
        return self.forward(mel_spectrogram)

# Convert text to phonemes
def text_to_phonemes(text):
    g2p = G2p()
    phonemes = g2p(text)
    phoneme_sequence = ' '.join(phonemes)
    print(f"Phoneme sequence: {phoneme_sequence}")
    return phoneme_sequence

# Mock function to simulate Tacotron2's output for Mel spectrogram
def phonemes_to_mel_spectrogram(phoneme_sequence):
    # Return a fixed-size random tensor as a placeholder
    return torch.randn(1, 10, 100)  # Example mel spectrogram shape

# Vocoder class to load the trained model and generate audio
class Vocoder:
    def __init__(self, model_path):  # Corrected the method name to __init__
        self.model = VocoderModel()
        try:
            checkpoint = torch.load(model_path)
            print(f"Loading model from {model_path}...")
            self.model.load_state_dict(checkpoint, strict=False)
            self.model.eval()  # Set model to evaluation mode
            print(f"Vocoder model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None

    def infer(self, mel_spectrogram):
        if self.model:
            with torch.no_grad():
                # Flatten mel spectrogram to match input size for the model
                batch_size, channels, time_steps = mel_spectrogram.shape
                mel_spectrogram = mel_spectrogram.view(batch_size, -1)  # Flatten to (batch_size, 1000)
                print(f"Mel spectrogram reshaped to: {mel_spectrogram.shape}")

                # Perform inference
                audio_waveform = self.model.infer(mel_spectrogram)
                return audio_waveform
        else:
            raise ValueError("Model not loaded properly. Cannot perform inference.")

# Save audio to a .wav file
def save_audio(audio_waveform, output_path):
    audio_waveform = audio_waveform.squeeze().cpu().numpy()  # Convert to NumPy array
    write(output_path, 22050, audio_waveform)  # Save audio at 22050 Hz
    print(f"Audio saved to {output_path}")

# Main Text-to-Speech function
def text_to_speech(input_text, vocoder_model_path, output_audio_path):
    print(f"Processing text: {input_text}")
    
    # Step 1: Convert text to phonemes
    phoneme_sequence = text_to_phonemes(input_text)
    
    # Step 2: Generate mel spectrogram from phonemes (using Tacotron2 or another TTS model)
    mel_spectrogram = phonemes_to_mel_spectrogram(phoneme_sequence)
    print(f"Generated Mel spectrogram: {mel_spectrogram.shape}")
    
    # Step 3: Load the vocoder model and generate the audio waveform
    vocoder = Vocoder(vocoder_model_path)
    try:
        audio_waveform = vocoder.infer(mel_spectrogram)
        
        # Step 4: Save the generated audio as a .wav file
        save_audio(audio_waveform, output_audio_path)
    except Exception as e:
        print(f"Error during inference: {e}")

# Example usage
input_text = "Hello, how are you?"  # Example input text
vocoder_model_path = "C:\\Mini_Project\\trained_model.pth"  # Path to your trained vocoder model
output_audio_path = "C:\\Mini_Project\\output\\output_audio.wav"  # Path to save the output audio

text_to_speech(input_text, vocoder_model_path, output_audio_path)
