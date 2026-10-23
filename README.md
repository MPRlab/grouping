# Setup procedure

The repo has two separate Python environments, because the training code is pinned to TensorFlow 1.10
(Python 3.6) while the web app runs on current, patched versions of Flask:

| Environment | Used for | Python | Requirements |
|---|---|---|---|
| web app | the study interface in `interface/` | 3.10+ | `interface/requirements.txt` |
| training | `madmom/`, `response_processing/`, `sample_generator/`, `mturk_scripts/` | 3.6 | `requirements.txt` |

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
    python3.6 -m venv venv
    source venv/bin/activate
    sudo apt-get install portaudio19-dev
    pip install -r requirements.txt

# Dumping the database of responses

 - SSH onto the server
 - `flask dumpdb --outfile my_outfile.json`
