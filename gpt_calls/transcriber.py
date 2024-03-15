import openai
import os

# Set up OpenAI API credentials

class Transcription:
    def __init__(self, file_location, output_folder, name, client):
        self.file_location = file_location
        self.output_folder = output_folder
        self.name = name
        self.audio_file_name = name + "_audio.wav"
        self.client = client

    def transcribe_audio(self):
        # Get the raw audio file path
        audio_file_path = os.path.join(self.file_location, self.audio_file_name)

        # Read the audio file
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        # Call the OpenAI API to transcribe the audio
        try:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_data,
                response_format="text"
            )

            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)

            # Save the transcription to a text file
            output_file_path = os.path.join(self.output_folder, f"{self.name}_transcript.txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(response.text)
        except Exception as e:
            print(f"An error occurred: {e}")

