from openai import OpenAI
import os


class Summarizer:
    def __init__(self, file_location, output_folder, name, client):
        self.file_location = file_location
        self.output_folder = output_folder
        self.name = name
        #self.transcript_name = transcript_file_name
        self.client = client

    def read_transcript(self):
        """Reads the transcript text from a file."""
        transcript_file_path = os.path.join(self.file_location, f"{self.name}_transcript.txt")
        with open(transcript_file_path, 'r') as file:
            return file.read()

    def summarize_transcript(self):
        # Get the transcript file path

        transcript_text = self.read_transcript()
        
        # Call the OpenAI API to summarize the transcript
        try:
            print("Summarizing transcript...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                message = [{"role": "assistant", "content": transcript_text}]
            )
            print("Transcript summarized.")
            response_text = response.choices[0].message['content']
            # Create the output folder if it doesn't exist
            os.makedirs(self.output_folder, exist_ok=True)
            # Save the summary to a text file
            output_file_path = os.path.join(self.output_folder, f"{self.name}_summary.txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(response_text)

        except Exception as e:
            print(f"An error occurred: {e}")