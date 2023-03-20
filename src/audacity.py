import os
import time

from printer import printer

class Audacity:

    def __init__(self, config_file):
        """Class to handle Audacity commands

        Args:
            config_file (dict): Config file
        """        
        printer('Loading DAW')
        self.config = config_file
        self.sd = self.config["step_directory"] 
        self.process_dir = self.sd["main_dir"] 
        self.src_dir = self.process_dir + self.sd["steps"]["raw"] 
        self.filename = 'podcast_raw.mp3'
        self.run_command('cd ~/../../Applications/ ; open -g Audacity.app/ ; cd ~')
        time.sleep(6)
        PIPE_TO_AUDACITY = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        PIPE_FROM_AUDACITY = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        self.topipe = open(PIPE_TO_AUDACITY, 'w')
        self.frompipe = open(PIPE_FROM_AUDACITY, 'r')
        self.eol = '\n'
        self.record_counter = 0

    def run_command(self, command):
        """Run a command in the terminal

        Args:
            command (str): The command to run
        """        
        os.system(command)

    def open_audacity(self):
        """
        Open Audacity from the terminal
        """     
        self.run_command('cd ~/../../Applications/ ; open -g Audacity.app/ ; cd ~')
        time.sleep(1)

    def close_audacity(self):
        """
        Close Audacity from the terminal
        """
        self.run_command("osascript -e 'quit app \"Audacity\"'")
        time.sleep(1)

    def send_command(self, command):
        """
        Send a command to Audacity
        """
        self.topipe.write(command + self.eol)
        self.topipe.flush()

    def get_response(self):
        """
        Get the response from Audacity
        """
        line = self.frompipe.readline()
        result = ""
        while True:
            result += line
            line = self.frompipe.readline()
            if line == '\n':
                return result

    def do_command(self, command):
        """Send a command to Audacity and gets the response

        Args:
            command (str): Command to send to Audacity

        Returns:
            str: Response from Audacity
        """        
        self.send_command(command)
        response = self.get_response()
        return response

    def rescan_devices(self):
        """
        Rescan audio devices in Audacity
        """
        self.do_command("RescanDevices")
        time.sleep(1)

    def scan_devices(self):
        """
        Scan input audio devices in Audacity
        """
        self.do_command("InputDevice")

    def scan_devices_out(self):
        """
        Scan output audio devices in Audacity
        """
        self.do_command("OutputDevice")

    def record(self):
        """
        Record audio in Audacity
        """
        self.do_command('CursTrackStart')
        self.do_command("Record2ndChoice")
        self.record_counter += 1

    def stop_record(self):
        """
        Stop recording audio in Audacity
        """
        self.do_command("Pause")

    def collapse_tracks(self):
        """
        Collapse all tracks in Audacity
        """
        self.do_command('CollapseAllTracks')

    def scan_device(self):
        """
        Handles the audio device selection in Audacity
        """
        self.run_command('cd ~ ; cd ../.. ; cd Applications/ ; open Audacity.app/')
        self.run_command('cd ~')
        self.run_command('open -a Terminal.app')
        self.rescan_devices()
        time.sleep(1)
        self.scan_devices()
        self.scan_devices_out()
        printer('Audio Device Selected\n')
        self.run_command("osascript -e 'quit app \"Audacity\"'")
        time.sleep(2)
        # self.run_command('cd ~ ; cd Desktop/soundcloud_process/ ; python main.py')

    def export(self, selection):
        """
        Export audio from Audacity to the
        raw directory in config file
        """
        track_selection = selection - 1
        self.do_command(f"Select: Track={track_selection} mode=Set")
        self.do_command("SelTrackStartToEnd")
        self.do_command(f"Export2: Filename={os.path.join(self.src_dir, self.filename)} NumChannels=1.0")

    def undo(self):
        """
        Undo the last command in Audacity
        """
        for _ in range(self.record_counter):
            self.do_command("Undo")