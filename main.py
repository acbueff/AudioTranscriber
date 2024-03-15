import subprocess
import sys
import platform
from utils.call_sink_script import call_script
from sink_capture import linuxSink
from gpt_calls import transcriber
from gpt_calls import client_gpt

#when running main, it should ask for user input. The input should be a number between 1 and 10

if __name__ == "__main__":
    os_name = platform.system()

    API_KEY = "acb123" #replace with actual API key

    #ask for user input
    user_input = input("Identify WP meeting. Enter a number between 1 and 10: ")
    #if number not between 1 and 10, ask again
    while not user_input.isdigit() or int(user_input) < 1 or int(user_input) > 10:
        user_input = input("Invalid input. Enter a number between 1 and 10: ")

    if os_name == "Windows":
        call_script("windows.py")
    elif os_name == "Linux":
        sink_object = linuxSink.LinuxSinkCapture(wp_meeting_number = user_input, application_name = "Chrome")
        sink_object.run()
        #call_script("linuxSink.py")
    else:
        print(f"Unsupported operating system: {os_name}")

    #After sink script is run, we should have raw audio .wav in /meeting_data/WP{wp_meeting_number}/raw_data/
    #We should then run the audio processing script on the raw audio file by creating a transcript
    #Create a transcript from the audio file using OpenAi api whisper
    #This will be done in the next part of the code
    #transcriber_object = transcriber.Transcription(file_location = sink_object.location, 
    #                                               output_folder = sink_object.location + f"/meeting_data/WP{user_input}/transcripts", 
    #                                               name = sink_object.name)
    transcriber_summary_object = client_gpt.ClientGPT(api_key = API_KEY, 
                                                      file_location = sink_object.location,
                                                      workpackage= user_input,
                                                      name = sink_object.name)