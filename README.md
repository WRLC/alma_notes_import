# Batch Update Alma Field by Barcode

This command line tool allows you to batch update a specific field in multiple Alma item records with a CSV file.

## Requirements

1. Command line terminal environment
1. Python 3.x

To check your local Python version, run:

`python --version`

If your system is running Python 2.x (e.g., Python 2.7.16), check if Python 3 is installed, too:

`python3 --version`

The deployment instructions in the next section assume your system's `python` and `pip` commands use Python 3.x. If not, substitute `python3` and `pip3`.)


## Deploying the tool

The tool runs locally via terminal command line, so you'll need to clone the app to your machine:

`git clone git@github.com:WRLC/alma_notes_import.git`

Then create/start a Python virtual environment and install dependencies:

```
cd alma_notes_import
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

You also need to copy the settings template so the tool will have all necessary information about your Alma environment:

`cp settings.template.py settings.py`

Edit `settings.py` to use your desired variables:

* `ALMA_SERVER`<br />The base URL for your Alma API endpoint (e.g., 'https://api-na.hosted.exlibrisgroup.com').

* `ALMA_API_KEY`<br />A read/write key for the Alma environment you wish to update.

* `DESTINATION_FIELD`<br />The field in the item record that you want to update (e.g., 'internal_note_3').

You can change the values in `settings.py` anytime, so you're not locked into whatever you set now.

Finally, make sure the `import.py` script is executable:

`chmod u+x import.py`

## CSV file

Your CSV file should contain only two columns:

1. Item barcode (for the item record you wish to update)
1. New field value (to insert into that item record)

The CSV file should NOT contain a header row. (If it does, you'll receive an error on the first row. However, all remaining rows will still be parsed.)

## Using the tool

If it's not already active, activate the Python virtual environment you created during deployment:

`source venv/bin/activate`

Run the `import.py` command as an executable with your CSV file as the only argument:

`./import.py /path/to/file.csv`

As it's running, you'll be notified of any barcodes that either can't be retrieved from the barcode or can't be updated with the new field value.

When the tool finishes, it will provide a completion message:

`Import complete. All submitted barcodes (except any errors listed above) have been updated in Alma.`