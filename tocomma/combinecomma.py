import csv
import itertools
import logging

# Set up logging
logging.basicConfig(filename='uncomma-900-999.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Open the input CSV file
with open('uncomma/uncomma-900-999.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Ensure fieldnames (headers) are stripped of any unwanted spaces
    reader.fieldnames = [field.strip() for field in reader.fieldnames]

    # Group the rows by controlno (converted to string), Title, Author, Callno, and Copyright
    groups = itertools.groupby(
        sorted(reader, key=lambda x: (str(x['controlno']), x['Title'], x['Author'], x['Callno'], x['Copyright'])), 
        key=lambda x: (str(x['controlno']), x['Title'], x['Author'], x['Callno'], x['Copyright'])
    )

    # Open the output CSV file
    with open('900-999.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the header row, adding the 'Quantity' column
        writer.writerow(['controlno', 'Title', 'Author', 'Callno', 'Accession', 'Copyright', 'Quantity'])

        # Process each group
        for key, group in groups:
            try:
                group_list = list(group)  # Convert group iterator to a list to iterate multiple times
                accessions = [row['Accession'] for row in group_list]
                quantity = len(accessions)  # Calculate the number of accessions
                title = "'" + key[1] + "'"  # Add apostrophes around the title
                row = [key[0], title, key[2], key[3], ', '.join(accessions), key[4], quantity]
                writer.writerow(row)
                logging.info(f"Successfully processed row: {row}")
            except Exception as e:
                logging.error(f"Error processing row: {key} - {e}")
