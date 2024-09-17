import csv
import itertools
import logging

# Set up logging
logging.basicConfig(filename='uncomma-100-299.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Helper function to create a range string for accession numbers
def accession_range(accessions):
    accessions = sorted(set(map(int, accessions)))  # Ensure accessions are integers and sorted
    if len(accessions) == 1:
        return str(accessions[0])  # If there's only one accession, return it as-is
    else:
        return f"{accessions[0]}-{accessions[-1]}"  # Return range from first to last accession

# Open the input CSV file
with open('uncomma/uncomma-100-299.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Ensure fieldnames (headers) are stripped of any unwanted spaces
    reader.fieldnames = [field.strip() for field in reader.fieldnames]

    # Group the rows by controlno (converted to string), Title, Author, Callno, and Copyright
    groups = itertools.groupby(
        sorted(reader, key=lambda x: (str(x['controlno']), x['Title'], x['Author'], x['Callno'], x['Copyright'])), 
        key=lambda x: (str(x['controlno']), x['Title'], x['Author'], x['Callno'], x['Copyright'])
    )

    # Open the output CSV file
    with open('100-299.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write the header row, adding the 'Quantity' column
        writer.writerow(['controlno', 'Title', 'Author', 'Callno', 'Accession', 'Copyright', 'Quantity'])

        # Process each group
        for key, group in groups:
            try:
                group_list = list(group)  # Convert group iterator to a list to iterate multiple times
                accessions = [row['Accession'] for row in group_list]
                quantity = len(accessions)  # Calculate the number of accessions

                # Create accession range string
                accession_str = accession_range(accessions)
                title = "'" + key[1] + "'"  # Add apostrophes around the title
                row = [key[0], title, key[2], key[3], accession_str, key[4], quantity]
                writer.writerow(row)
                logging.info(f"Successfully processed row: {row}")
            except Exception as e:
                logging.error(f"Error processing row: {key} - {e}")
