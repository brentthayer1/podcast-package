import os
from process_audio import ProcessRegistry

from audacity import Audacity
from soundcloud import SoundcloudEngine

class PodcastHandler:

    def __init__(self, start_step, config_file, record):
        """Handles the podcast creation process

        Args:
            start_step (str): Step to start the process
            config_file (dict): Config file
            record (bool): Record audio or not
        """        
        self.start_step = start_step
        self.config_file = config_file
        if record:
            self.audacity = Audacity(config_file)
        
        self.soundcloud = SoundcloudEngine(self.config_file)
        
    def run_command(self, command):
        """Run a command in the terminal

        Args:
            command (str): Command to run
        """       
        os.system(command)

    def process_audio(self, edit_start, edit_stop):
        """Run the audio processing steps

        Args:
            edit_start (int): Location to start edit
            edit_stop (int): Location to stop edit
        """        
        self.audio_processor = ProcessRegistry(self.start_step)(self.config_file)
        self.audio_processor.process(edit_start, edit_stop)
    
    def initialize_audacity(self):
        """
        Handle the initialization of Audacity.
        Scan devices, rescan devices, close Audacity
        and reopen it
        """
        self.audacity.rescan_devices()
        self.audacity.scan_devices()
        self.audacity.scan_devices_out()
        self.audacity.close_audacity()
        self.audacity = Audacity(self.config_file)
