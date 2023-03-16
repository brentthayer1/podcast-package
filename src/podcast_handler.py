import os
from process_audio import ProcessRegistry

from audacity import Audacity
from soundcloud import SoundcloudEngine

class PodcastHandler:
    def __init__(self, start_step, config_file, record):
        self.start_step = start_step
        self.config_file = config_file
        if record:
            self.audacity = Audacity(config_file)
        
        self.soundcloud = SoundcloudEngine(self.config_file)
        
    def run_command(self, command):
        os.system(command)

    def process_audio(self, edit_start, edit_stop):
        self.audio_processor = ProcessRegistry(self.start_step)(self.config_file)
        self.audio_processor.process(edit_start, edit_stop)
    
    def initialize_audacity(self):
        self.audacity.rescan_devices()
        self.audacity.scan_devices()
        self.audacity.scan_devices_out()
        self.audacity.close_audacity()
        self.audacity = Audacity(self.config_file)
