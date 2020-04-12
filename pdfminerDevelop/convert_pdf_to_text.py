# Doc: https://pdfminersix.readthedocs.io/en/latest/tutorials/highlevel.html

from pdfminer import high_level
import sys
import os
import collections

import tempfile
from google.cloud import storage
storage_client = storage.Client()


def get_ancestries(data):
    print(f'Starting analysis...')
    file_data = data

    file_name = file_data['name']
    bucket_name = file_data['bucket']

    blob = storage_client.bucket(bucket_name).get_blob(file_name)

    # Analyze text
    print(f'Analyzing {file_name}.')
    return __extract_pdf_as_text(blob)


def __extract_pdf_as_text(current_blob):
    # [START PubSub Code]
    print(f'Extracting PDF file...')
    file_name = current_blob.name
    _, temp_local_filename = tempfile.mkstemp()

    # Download file from bucket.
    current_blob.download_to_filename(temp_local_filename)
    print(f'PDF {file_name} was downloaded to {temp_local_filename}.')
    # [END PubSub Code]

    # Open the PDF file and check for ancestry terms
    text = high_level.extract_text(temp_local_filename)

    # Option 3
    ancestries = ['aboriginal australian', 'african american', 'afro-caribbean',
                  'afican', 'asian', 'central asian', 'circumpolar peoples',
                  'east asian', 'european', 'greater middle eastern', 'north arican',
                  'persian', 'hispanic', 'latin american', 'native american', 'oceanain',
                  'admixed', 'south asian', 'south east asian', 'sub-sharan african']
    lines = text.split("\n")
    lc_lines = [line.lower() for line in lines]

    # Create file for results
    output_file_name = 'ancestry_result_analysis.txt'
    file = open(output_file_name, "w")

    for ancestry in ancestries:
        for index, sentence in enumerate(lc_lines):
            # Check if sentence has at least a partial match
            if ancestry in sentence:
                # print(f'\nPart match  -- A: {ancestry} -- L: {lc_lines[index]}')
                file.write(
                    '\nPart match to Ancestry term: ' + ancestry + ' -- Line: ' + lc_lines[index])
                # Confirm exact match to word in sentence
                for word in lc_lines[index].split(' '):
                    if ancestry == word:
                        # print(f'Exact match -- A: {ancestry} -- L: {lc_lines[index]}')
                        file.write(
                            '\nExact match to Ancestry term: ' + ancestry + ' -- Line: ' + lc_lines[index])
                file.write('\n')
    # Close file
    file.close()

    # [START PubSub Code]
    # Upload result to a second bucket, to avoid re-triggering the function.
    # You could instead re-upload it to the same bucket + tell your function
    # to ignore files marked as blurred (e.g. those with a "blurred" prefix)

    output_bucket_name = 'results-' + file_name.split('.')[0] + '.txt'

    blur_bucket_name = os.getenv('BLURRED_BUCKET_NAME')
    blur_bucket = storage_client.bucket(blur_bucket_name)
    new_blob = blur_bucket.blob(output_bucket_name)  # was file_name
    new_blob.upload_from_filename(output_file_name)
    print(f'Results uploaded to: gs://{blur_bucket_name}/{output_bucket_name}')

    # Delete the temporary file.
    os.remove(temp_local_filename)
    # [END PubSub Code]


# if __name__ == '__main__':
#     extract_pdf_as_text()
