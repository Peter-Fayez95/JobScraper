import pandas as pd
from datetime import datetime
import json
import os

def save_to_csv(jobs_data, filename=None, default_value="N/A"):
    """
    Save the scraped job data to a CSV file.
    
    Parameters:
    - jobs_data (dict/list): The scraped job data
    - filename (str): Optional custom filename
    - default_value (str): Value to use for missing fields
    
    Returns:
    - str: Path to the saved CSV file
    """
    if not filename:
        output_dir = os.getenv("OUTPUT_DIR", "")
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"jobs_{timestamp}.csv") if output_dir else f"jobs_{timestamp}.csv"
    
    # Process the data to extract jobs
    jobs = []
    
    # First, check if content is a string that needs to be parsed as JSON
    if isinstance(jobs_data, dict) and "content" in jobs_data:
        content = jobs_data["content"]
        if isinstance(content, str):
            try:
                # Try to parse the content as JSON
                parsed_content = json.loads(content)
                if isinstance(parsed_content, list):
                    jobs = parsed_content
                elif isinstance(parsed_content, dict):
                    if "jobs" in parsed_content:
                        jobs = parsed_content["jobs"]
                    else:
                        jobs = [parsed_content]
            except json.JSONDecodeError:
                print("Could not parse content as JSON")
    
    # If no jobs found yet, try standard extraction methods
    if not jobs:
        # Try to find jobs in the data structure
        if isinstance(jobs_data, dict):
            if "data" in jobs_data:
                data = jobs_data["data"]
                
                # Handle different possible structures
                if isinstance(data, list):
                    # Case 1: List of job items
                    jobs = data
                elif isinstance(data, dict):
                    # Case 2: Data contains a jobs list
                    if "jobs" in data:
                        jobs = data["jobs"]
                    # Case 3: Data is a single job
                    elif "title" in data:
                        jobs = [data]
            
            # Case 4: Direct jobs list
            elif "jobs" in jobs_data:
                jobs = jobs_data["jobs"]
    
    # If jobs is empty or not found, search for job-like structures
    if not jobs and isinstance(jobs_data, dict):
        for key, value in jobs_data.items():
            if key.lower() in ["jobs", "positions", "listings", "results"]:
                if isinstance(value, list):
                    jobs = value
                    break
    
    # If we have jobs, create a DataFrame
    if jobs:
        # Create DataFrame directly from the jobs list
        df = pd.DataFrame(jobs)
        
        # Replace any None or empty values with N/A
        df.fillna(default_value, inplace=True)
        
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"Saved {len(jobs)} jobs to {filename}")
        return filename
    
    # If no valid jobs data found
    print("No structured job data found to save to CSV")
    
    # Save the raw data as a backup
    backup_dir = os.getenv("BACKUP_DIR", "")
    if backup_dir and not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    backup_filename = os.path.join(backup_dir, f"raw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json") if backup_dir else f"raw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(backup_filename, 'w') as f:
        json.dump(jobs_data, f, indent=4)
    print(f"Saved raw data to {backup_filename}")
    
    return None