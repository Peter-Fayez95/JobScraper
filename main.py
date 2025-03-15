from scraper import run_scraper
import json
from csv_handler import save_to_csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # Run the pipeline
    result = run_scraper()
    
    # Print the result
    print(json.dumps(result, indent=4))
    
    # Save to CSV with "N/A" as the default value for missing fields
    csv_file = save_to_csv(result, default_value="N/A")
    
    if csv_file:
        print(f"Successfully saved jobs to {csv_file}")
    else:
        print("Could not save jobs to CSV - check the raw data file")
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()