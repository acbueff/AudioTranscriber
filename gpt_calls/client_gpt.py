import openai
import os
import gpt_calls.transcriber as transcriber
import gpt_calls.summarizer as summarizer


class ClientGPT:
    def __init__(self, api_key, file_location, workpackage, name):
        self.api_key = api_key
        self.file_location = file_location
        self.workpackage = f"WP{workpackage}"
        self.client = openai.OpenAI(api_key=self.api_key)
        self.name = name
        self.raw_file_location = os.path.join(self.file_location, f"meeting_data/{self.workpackage}/raw_data")
        self.raw_data_name = f"{self.name}.wav"
        self.transcript_file_location = os.path.join(self.file_location, f"meeting_data/{self.workpackage}/transcripts")
        self.transcript_file_name = f"{self.name}_transcript.txt"
        self.summary_file_location = os.path.join(self.file_location, f"meeting_data/{self.workpackage}/whisper_summary")

    
    def main(self):

        try:
            transcriber_object = transcriber.Transcription(file_location = self.raw_file_location,
                                                            output_folder = self.transcript_file_location, 
                                                            name = self.name,
                                                            client = self.client)
            transcriber_object.transcribe_audio()

            summary_object = summarizer.Summarizer(file_location = self.transcript_file_location, 
                                                   output_folder = self.summary_file_location, 
                                                   name = self.name,
                                                   client = self.client)
            summary_object.summarize_transcript()
            
        except Exception as e:
            print(f"An error occurred: {e}")