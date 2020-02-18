#!/usr/bin/env python

import csv
import requests
import sys
import json

from settings import *

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rowNumber = 1

    # Iterate through each row of the CSV
    for row in csv_reader:
        barcode = row[0]  # Column 1 = barcode
        note = row[1]  # Column 2 = value to insert as a note

        # Get item record from barcode via requests
        try:
            r = requests.get(ALMA_SERVER + '/almaws/v1/items', params={
                'apikey': ALMA_API_KEY,
                'item_barcode': barcode,
                'format': 'json'
            })

            # Provide for reporting HTTP errors
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:

            # If HTTP error, inform user
            print('Barcode ' + str(barcode) + ' in row ' + str(rowNumber) + ' not found.')

            # Bump the row number up before exiting
            rowNumber = rowNumber + 1

            # Stop processing this row
            continue

        # If request good, parse JSON into a variable
        itemRec = r.json()

        # Insert column 2 value into the destination field
        itemRec['item_data'][DESTINATION_FIELD] = note

        # Specify JSON content type for PUT request
        headers = {'content-type': 'application/json'}

        # Get IDs from item record for building PUT request endpoint
        mms_id = itemRec['bib_data']['mms_id']  # Bib ID
        holding_id = itemRec['holding_data']['holding_id']  # Holding ID
        item_pid = itemRec['item_data']['pid']  # Item ID

        # Construct API endpoint for PUT request from item record data
        putEndpoint = '/almaws/v1/bibs/' + mms_id + '/holdings/' + holding_id + '/items/' + item_pid

        # send full updated JSON item record via PUT request
        try:
            r = requests.put(ALMA_SERVER + putEndpoint, params={
                'apikey': ALMA_API_KEY
            }, data=json.dumps(itemRec), headers=headers)

            # Provide for reporting HTTP errors
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:

            # If HTTP error, inform user
            print('Barcode ' + str(barcode) + ' in row ' + str(rowNumber) + ' could not be updated.')

            # Bump the row number up before exiting
            rowNumber = rowNumber + 1

            # Stop processing this row
            continue

        # Bump the row number up before going to next row
        rowNumber = rowNumber + 1

# Provide import info as output to command line
print('Import complete. All submitted barcodes (except any errors listed above) have been updated in Alma.')
