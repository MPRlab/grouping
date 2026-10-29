# Setup procedure

The repo has two separate Python environments, one for the study web app and one for training and analysis
(TensorFlow 2.21):

| Environment | Used for | Python | Requirements |
|---|---|---|---|
| web app | the study interface in `interface/` | 3.10+ | `interface/requirements.txt` |
| training | `madmom/`, `response_processing/`, `sample_generator/`, `mturk_scripts/` | 3.12 or 3.13 | `requirements.txt` (`requirements-ace.txt` on the ACE GPU cluster) |

## Web app

Create a virtual environment and install the dependencies:

    cd /path/to/grouping
    python3 -m venv interface/venv
    source interface/venv/bin/activate
    pip install -r interface/requirements.txt

Secrets are read from environment variables (do not commit them):

    export GROUPING_SECRET_KEY=<long random string>        # e.g. python -c "import secrets; print(secrets.token_hex(32))"
    export GROUPING_ADMIN_USERNAME=<username for /manage>
    export GROUPING_ADMIN_PASSWORD=<password for /manage>

The `/manage` page (which can add/remove samples from the live study) requires HTTP basic auth with those
credentials, and is disabled if they are not set. Only serve it over HTTPS.

Create the database (this deletes any existing data, so read the warning before confirming):

    export FLASK_APP=/path/to/grouping/interface/interface/interface.py
    mkdir -p interface/interface/db
    flask initdb

Then choose which samples are in the study, either on the `/manage` page or from the command line with
`flask load <directory>` (the directory must be inside `/var/www/html/grouping`). Responses are only
accepted for samples that are in the study.

You can now run the webapp with

    flask run

To avoid repeating the setup in every shell, you can add the `source .../activate` and `export FLASK_APP=...`
lines above to the end of your `.bashrc`, using the path where you cloned the repo.

## Training and analysis

    cd /path/to/grouping
    python3.12 -m venv venv
    source venv/bin/activate
    sudo apt-get install portaudio19-dev build-essential
    pip install -r requirements.txt

`requirements.txt` also installs the vendored `madmom` in editable mode, which compiles its Cython extensions
(hence `build-essential`, a C compiler).

The training scripts in `madmom/bin/` (`RhythmicGroupingRNN`, `RhythmicGroupingSimpleRNN`, `RhythmicGroupingCNN`)
were ported from TensorFlow 1.10 to TensorFlow 2. Checkpoints saved by the TensorFlow 1 versions cannot be loaded
by the new scripts, so retrain before running `test`.

# Dumping the database of responses

 - SSH onto the server
 - `flask dumpdb --outfile my_outfile.json`
