import os
import time
from pydub import AudioSegment
from datetime import date
import time
import json
import time  


class ProcessAudioBase:
    def __init__(self, config_file): 
        self.config = config_file
        self.sd = self.config["step_directory"] #!!!!
        self.process_dir = self.sd["main_dir"] #!!!!
        self.src_dir = self.process_dir + self.sd["steps"]["raw"] #!!!!
        self.file_name = [f[:-4] for f in os.listdir(self.src_dir) if '.mp3' in f][0] #!!!!
        self.get_dirs_and_files()

    def get_dirs_and_files(self):
        self.trimmed_dir = self.process_dir + self.sd["steps"]["trimmed"]
        self.high_passed_dir = self.process_dir + self.sd["steps"]["high_passed"]
        self.normalized1_dir = self.process_dir + self.sd["steps"]["normalized1"]
        self.compressed_dir = self.process_dir + self.sd["steps"]["compressed"]
        self.normalized2_dir = self.process_dir + self.sd["steps"]["normalized2"]
        self.compiled_dir = self.process_dir + self.sd["steps"]["compiled"]
        self.soundcloud_src_dir = self.process_dir + self.sd["steps"]["soundcloud_source"]
        self.raw_file = f'{self.src_dir}{self.file_name}.mp3'
        self.trimmed_file = f'{self.trimmed_dir}{self.file_name}_TRIMMED.mp3'
        self.high_passed_file = f'{self.high_passed_dir}{self.file_name}_HIGHPASSED.mp3'
        self.normalized1_file = f'{self.normalized1_dir}{self.file_name}_NORMALIZED1.mp3'
        self.compressed_file = f'{self.compressed_dir}{self.file_name}_COMPRESSED.mp3'
        self.normalized2_file = f'{self.normalized2_dir}{self.file_name}_NORMALIZED2.mp3'
        self.compiled_file = f'{self.compiled_dir}{self.file_name}_COMPILED.mp3'
        self.soundcloud_src_file = ''
        self.sermon_dir = self.config["sermon_dir"]
        self.podcast_dir = self.config["podcast_dir"]
        self.opener = self.config["opener"]
        self.closer = self.config["closer"]
        os.chdir(self.src_dir)
    
    def run_command(self, command):
        os.system(command)

    def remove(self, file):
        self.run_command(f'rm -f {file}')

    def sleep(self, t):
        time.sleep(t)

    def trim(self, start, stop):
        today = date.today()
        raw_file = AudioSegment.from_mp3(self.raw_file)
        raw_file.export(f'{self.sermon_dir}{self.file_name}_{today}_RAW.mp3')
        print('Copied Raw File To Sermons Directory')
        sliced_file = raw_file[start:stop]
        sliced_file.export(self.trimmed_file)
        print('Trim Complete')
        self.sleep(2)

    def high_pass(self, input, output):
        high_pass_config = self.config["process_audio"]["high_pass"]
        high_pass_freq = high_pass_config["freq"]
        self.run_command(
            f'ffmpeg -i {input} -af "highpass=f={high_pass_freq}" {output} -hide_banner -loglevel error'
        )
        print('High Pass Complete')
        self.remove(input)
        self.sleep(2)

    def normalize(self, input, output):
        normalize_config = self.config["process_audio"]["normalize"]
        I = normalize_config["I"]
        LRA = normalize_config["LRA"]
        TP = normalize_config["TP"]
        self.run_command(
            f'ffmpeg -i {input} -af loudnorm=I={I}:LRA={LRA}:TP={TP} -ar 48k {output} -hide_banner -loglevel error'
        )
        print('Normalization Complete')
        self.remove(input)
        self.sleep(2)

    def compress(self, input, output):
        compress_config = self.config["process_audio"]["compress"]
        threshold = compress_config["threshold"]
        ratio = compress_config["ratio"]
        attack = compress_config["attack"]
        release = compress_config["release"]

        self.run_command(
            f'ffmpeg -i {input} -af acompressor=threshold={threshold}:ratio={ratio}:attack={attack}:release={release} {output} -hide_banner -loglevel error'
        )
        print('Compression Complete')
        self.remove(input)
        self.sleep(2)

    def compile(self, input, output):
        opener = AudioSegment.from_mp3(self.opener)
        closer = AudioSegment.from_mp3(self.closer)
        sermon = AudioSegment.from_mp3(input)
        opener_length = opener.duration_seconds * 1000
        closer_length = closer.duration_seconds * 1000
        sermon_length = sermon.duration_seconds * 1000
        opener_spot = 0
        sermon_spot = opener_length - 20000
        closer_spot = sermon_spot + sermon_length - 15000
        final_length = closer_spot + closer_length
        blank_track = AudioSegment.silent(duration=final_length)
        blank_track = blank_track.overlay(opener, position=opener_spot)
        blank_track = blank_track.overlay(sermon, position=sermon_spot)
        blank_track = blank_track.overlay(closer, position=closer_spot)
        blank_track.export(output, format='mp3')
        print('Compile Complete')
        self.remove(input)
        self.sleep(2)

    def stage(self, input):
        time_stamp = time.time()
        self.soundcloud_src_file = f'{self.soundcloud_src_dir}{self.file_name}_{str(time_stamp)[:9]}.mp3'
        final_file = AudioSegment.from_mp3(input)
        final_file.export(self.soundcloud_src_file)
        print('Copied to Staging Directory')
        self.remove(input)
        self.sleep(2)

class ProcessAudioFull(ProcessAudioBase):
    def __init__(self, config_file):
        self.config = config_file
        self.sd = self.config["step_directory"]
        self.process_dir = self.sd["main_dir"]
        self.src_dir = self.process_dir + self.sd["steps"]["raw"]
        self.file_name = [f[:-4] for f in os.listdir(self.src_dir) if '.mp3' in f][0]
        self.get_dirs_and_files()

    def process(self, start, stop):
        self.trim(start, stop)
        self.high_pass(self.trimmed_file, self.high_passed_file)
        self.normalize(self.high_passed_file, self.normalized1_file)
        self.compress(self.normalized1_file, self.compressed_file)
        self.normalize(self.compressed_file, self.normalized2_file)
        self.compile(self.normalized2_file, self.compiled_file)
        self.stage(self.compiled_file)

class ProcessAudioCompress(ProcessAudioBase):
    def __init__(self, config_file):
        self.config = config_file
        self.sd = self.config["step_directory"] #!!!!
        self.process_dir = self.sd["main_dir"] #!!!!
        self.src_dir = self.process_dir + self.sd["steps"]["compressed"] #!!!!
        self.file_name = ["_".join(f[:-4].split("_")[:-1]) for f in os.listdir(self.src_dir) if '.mp3' in f][0] #!!!!
        self.get_dirs_and_files()

    def process(self, start, stop):
        print('AAAAAAA')
        self.normalize(self.compressed_file, self.normalized2_file)
        self.compile(self.normalized2_file, self.compiled_file)
        self.stage(self.compiled_file)

def ProcessRegistry(process):
    registry = {
        "full" : ProcessAudioFull,
        "compress": ProcessAudioCompress
    }

    return registry[process]



