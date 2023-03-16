import os
import sys
import click
import json

from podcast_handler import PodcastHandler

CONFIG_FILE = "../config.json"
    
@click.command()
@click.option("--start-step", default="full")
def main(start_step):
    """
    Main function for the podcast script
    to start the podcast process at a specific step

    Args:
        start_step (str): Step to start the process at
    """    
    with open(CONFIG_FILE) as json_file:
        config_file = json.load(json_file)

    record = False
    if start_step == "full":
        record = True

    if start_step == "full-no-record":
        start_step == "full"

    handler = PodcastHandler(start_step, config_file, record)

    while True:
        if record:
            handler.initialize_audacity()
            recordstart = input('Start Recording New Track? [y]es / [n]o: ')
            if recordstart == 'y':
                handler.audacity.record()
                handler.audacity.collapse_tracks()
                input('Press [ENTER] To Stop Recording')
                handler.audacity.stop_record()
                export_confirm = input('Select A Recorded Track To Export? [y]es / [n]o: ')
                if export_confirm == 'n':
                    continue
                elif export_confirm == 'y':
                    handler.run_command(f'rm -f {os.path.join(handler.audacity.src_dir, handler.audacity.filename)}')
                    export_selection = int(input('Track Number To Export: '))
                    handler.audacity.export(export_selection)
                else:
                    print('Select \'y\' or \'n\'')
                    continue

            elif recordstart == 'n':
                pass
            else:
                print('Select \'y\' or \'n\'')
                continue
        
        process_audio = input(f"Process Audio in {handler.audacity.src_dir} ? [y]es / [n]o: ")
        if process_audio == "y":
            edit_start = int(input('Select [SECONDS] Marker For Beginning: ')) * 1000
            edit_stop = int(input('Select [SECONDS] Marker For Ending: ')) * 1000
            print(f'This Track Will Be Edited From\n{int(edit_start/1000)} Seconds To {int(edit_stop/1000)} Seconds')
            handler.process_audio(edit_start, edit_stop)
        elif process_audio == "n":
            continue
        else:
            print('Select \'y\' or \'n\'')
            continue

        upload_to_soundcloud = input('Proceed With Upload To SoundCloud? [y]es / [n]o: ')
        if upload_to_soundcloud == 'y': 
            title = input("Track title: ")
            handler.soundcloud.upload(title=title, artwork=handler.config_file["image"]
                                      )
        elif upload_to_soundcloud == 'n':
            print('Please Record Another Track,\nChange Your Track Selection,\nOr Change Your Track Edit Selections')
            continue
        else:
            print('Please Select \'y\' or \'n\'...')
            continue

        exit_program = input('\nPress [ENTER] To Exit Podcast Program')
        if record:
            handler.audacity.undo()
        handler.run_command("osascript -e 'quit app \"Audacity\"'")
        sys.exit()

if __name__ == "__main__":
    main()
