import subprocess
import signal
import time
import os

class LinuxSinkCapture:
    def __init__(self, wp_meeting_number = 1, application_name = "Chrome"):
        #Get the current data format YYYYMMDD
        self.date = time.strftime("%Y%m%d")
        #get the current time to the minute
        self.time = time.strftime("%H%M")

        self.date_time = self.date + "_" + self.time
        self.virtual_sink_name = application_name + "VirtualSink"
        self.name =f"{self.date_time}_WP{wp_meeting_number}"
        self.audio_file_name = f"{self.date_time}_WP{wp_meeting_number}_audio.wav"
        #output file will direct to meeting_data/WP{wp_meeting_number}/raw_data/self.audio_file_name
        self.location = os.getcwd()
        self.output_file = self.location + f"/meeting_data/WP{wp_meeting_number}/raw_data/{self.audio_file_name}"  # Modify this line with your desired path

    def get_physical_sink_name(self):
        result = subprocess.run(["pactl", "list", "short", "sinks"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if 'alsa_output' in line:
                return line.split()[1]
        print("No physical sink found")
        return None

    def create_sinksOLD(self,virtual_sink_name, physical_sink_name):
        subprocess.run([
            "pactl", "load-module",
            "module-null-sink",
            f"sink_name={virtual_sink_name}",
            f"sink_properties=device.description=\"{virtual_sink_name}\""
        ])
        print(f"Created virtual sink: {virtual_sink_name}")

        subprocess.run([
            "pactl", "load-module",
            "module-combine-sink",
            f"sink_name=CombinedSink",
            f"slaves={virtual_sink_name},{physical_sink_name}"
        ])
        print(f"Created combined sink with {virtual_sink_name} and {physical_sink_name}")


    def create_sinks(self, virtual_sink_name, physical_sink_name):
        # Load module-null-sink and capture its ID
        load_null_sink_result = subprocess.run([
            "pactl", "load-module",
            "module-null-sink",
            f"sink_name={virtual_sink_name}",
            f"sink_properties=device.description=\"{virtual_sink_name}\""
        ], capture_output=True, text=True)
        null_sink_id = load_null_sink_result.stdout.strip()

        # Load module-combine-sink and capture its ID
        load_combine_sink_result = subprocess.run([
            "pactl", "load-module",
            "module-combine-sink",
            f"sink_name=CombinedSink",
            f"slaves={virtual_sink_name},{physical_sink_name}"
        ], capture_output=True, text=True)
        combine_sink_id = load_combine_sink_result.stdout.strip()

        print(f"Created virtual sink: {virtual_sink_name} with ID {null_sink_id}")
        print(f"Created combined sink with {virtual_sink_name} and {physical_sink_name} with ID {combine_sink_id}")

        # Return the IDs for later use
        return null_sink_id, combine_sink_id


    def record_audio_from_sink(self, sink_name, output_file):
        monitor_source = f"{sink_name}.monitor"
        parec_command = ['parec', '--format=s16le', '--rate=44100', '--channels=2', '--device', monitor_source]
        ffmpeg_command = ['ffmpeg', '-y', '-f', 's16le', '-ar', '44100', '-ac', '2', '-i', '-', output_file]

        parec_process = subprocess.Popen(parec_command, stdout=subprocess.PIPE)
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=parec_process.stdout)

        print("Recording audio output. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            parec_process.send_signal(signal.SIGINT)
            ffmpeg_process.wait()
            print(f"Recording saved to {output_file}")


    def unload_modules(self, module_ids):
        for module_id in module_ids:
            subprocess.run(["pactl", "unload-module", module_id])
            print(f"Unloaded module ID: {module_id}")



    def run(self):
        physical_sink_name = self.get_physical_sink_name()
        if physical_sink_name:
            print(f"Physical Sink Name: {physical_sink_name}")
            null_sink_id, combine_sink_id = self.create_sinks(self.virtual_sink_name, physical_sink_name)
            
            # Explicitly wait for user input before starting the recording. This gives time to set up playback in pavucontrol.
            input("Set up playback in pavucontrol then press Enter to start recording...")
            
            self.record_audio_from_sink(self.virtual_sink_name, self.output_file)
            
            # Explicitly wait for user input before unloading the modules. This ensures recording can be stopped properly.
            input("Press Enter to stop recording and unload modules...")
            
            self.unload_modules([null_sink_id, combine_sink_id])
        else:
            print("Unable to find physical audio sink. Exiting.")

