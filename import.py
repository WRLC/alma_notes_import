import csv
import requests
import sys

from settings import *

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rowNumber = 0

    # Iterate through each row of the CSV
    for row in csv_reader:
        barcode = row[0]  # Column 1 = barcode
        note = row[1]  # Column 2 = value to insert as a note

        # Get item record from barcode via requests
        try:
            r = requests.get(ALMA_SERVER + '/almaws/v1/items', params={
                'apikey': SCF_API_KEY,
                'item_barcode': barcode,
                'format': 'json'
            })
            itemRec = r.json()

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
            sys.exit(1)

        # Get IDs from item record for update request params
        mms_id = itemRec['bib_data']['mms_id']
        holding_id = itemRec['holding_data']['holding_id']
        item_pid = itemRec['item_data']['pid']

        # TODO: Update item record with note value from CSV

        # TODO: provide import info as output to command line

        rowNumber = rowNumber + 1
