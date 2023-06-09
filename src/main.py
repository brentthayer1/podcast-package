import os
import sys
import click
import json

from podcast_handler import PodcastHandler

from printer import printer

CONFIG_FILE = "../config.json"

def open_json_file(file):
    with open(file) as json_file:
        return json.load(json_file)
    
@click.command()
@click.option("--start-step", default="full")
def main(start_step):
    """
    Main function for the podcast script
    to start the podcast process at a specific step

    Args:
        start_step (str): Step to start the process at
    """    

    config_file = open_json_file(CONFIG_FILE)

    record = False
    if start_step == "full":
        record = True

    if start_step == "full-no-record":
        start_step == "full"

    handler = PodcastHandler(start_step, config_file, record)
    if record:
        handler.initialize_audacity()

    while True:
        if record:
            recordstart = printer('Start Recording New Track?', '[y]es / [n]o: ').lower()
            if recordstart == 'y':
                handler.audacity.record()
                handler.audacity.collapse_tracks()
                printer(None, 'Press [ENTER] To Stop Recording')
                handler.audacity.stop_record()
                export_confirm = printer('Select A Recorded Track To Export?', '[y]es / [n]o: ').lower()
                if export_confirm == 'n':
                    continue
                elif export_confirm == 'y':
                    handler.run_command(f'rm -f {os.path.join(handler.audacity.src_dir, handler.audacity.filename)}')
                    export_selection = int(printer(None, 'Track Number To Export: '))
                    handler.audacity.export(export_selection)
                else:
                    printer('Select \'y\' or \'n\'')
                    continue

            elif recordstart == 'n':
                pass
            else:
                printer('Select \'y\' or \'n\'')
                continue
        
        process_audio = printer(f'Process Audio?', '[y]es / [n]o: ').lower()
        if process_audio == "y":
            edit_start = int(printer(None, 'Select [SECONDS] Marker For Beginning: ')) * 1000
            edit_stop = int(printer(None, 'Select [SECONDS] Marker For Ending: ')) * 1000
            printer(f'This Track Will Be Edited From\n{int(edit_start/1000)} Seconds To {int(edit_stop/1000)} Seconds')
            handler.process_audio(edit_start, edit_stop)
        elif process_audio == "n":
            continue
        else:
            printer('Select \'y\' or \'n\'')
            continue

        upload_to_soundcloud = printer('Proceed With Upload To Soundcloud?', '[y]es / [n]o: ').lower()
        if upload_to_soundcloud == 'y': 
            title = printer(None, 'Podcast Title: ')
            handler.audio_processor.move_to_final_dir()
            handler.soundcloud.upload(title=title, artwork=handler.config_file["image"]
                                      )
        elif upload_to_soundcloud == 'n':
            printer('Please Record Another Track,\nChange Your Track Selection,\nOr Change Your Track Edit Selections')
            continue
        else:
            printer('Please Select \'y\' or \'n\'...')
            continue
        exit_program = printer(None, 'Press [ENTER] To Exit Podcast Program')
        if record:
            handler.audacity.undo()
        handler.run_command("osascript -e 'quit app \"Audacity\"'")
        sys.exit()

if __name__ == "__main__":
    main()
