# podcast-package

This project handles recording audio, processesing audio, and uploading audio to Soundcloud.

This projct depends on a few items.
First, audio is recorded through Audacity.  This needs to be installd separately.
Second, an active Soundcloud account is needed, as well an access token for Soundcloud.

## `config.json`
The config.json file holds configuration for all parts of this project.

- `sermon_dir` : This is the dirctory where raw recorded audio will be copied to prior to processesing.
- `podcast_dir` : This is the directory where processed and compiled audio will be copied to in addition to uploading to Soundcloud.
- `opener` : Location of the podcast opener track.
- `closer` : Location of the podcast closer track.
- `image` : Location of the podcast image to use.
- `main_dir` : Directory where podcast steps populate.
- `process_audio` : Configuration for process audio steps.
- `soundcloud` : Configuration for Soundcloud.