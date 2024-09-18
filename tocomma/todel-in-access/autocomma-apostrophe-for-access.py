import csv
import logging

# Set up logging
logging.basicConfig(filename='c-only-900-999.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def process_csv(input_file, output_file):
    try:
        # Open input CSV file
        with open(input_file, 'r') as infile:
            reader = csv.DictReader(infile)
            controlnos = []
            
            # Process each row and log it
            for row in reader:
                try:
                    controlno = f"'{row['controlno']}',"
                    controlnos.append(controlno)
                    logging.info(f"Successfully processed controlno: {controlno}")
                except KeyError as ke:
                    logging.error(f"Missing 'controlno' in row: {row}. Error: {ke}")
                except Exception as e:
                    logging.error(f"Error processing row: {row}. Error: {e}")

        # Write to output CSV file
        with open(output_file, 'w', newline='') as outfile:
            for controlno in controlnos:
                outfile.write(controlno + '\n')  # Directly write to file without extra quoting

        logging.info(f"Successfully processed {len(controlnos)} controlnos and saved to {output_file}.")
    except Exception as e:
        logging.error(f"Error processing file: {e}")

# Define file paths
input_file = 'controlno-only/controlNumber_only_900-999.csv'  # Your input CSV
output_file = 'to-access-900-999.csv'  # The output file

# Process the CSV
process_csv(input_file, output_file)

print(f"Processing completed. Check {output_file} for results and the log file for details.")
