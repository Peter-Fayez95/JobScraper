from scrapegraphai.graphs import SmartScraperGraph
import os

# Instructions for the scraper
SCRAPER_INSTRUCTIONS = """
Extract all job listings.
    For each job listing, collect:
    1. Job title
    2. Job ID
    3. Location
    4. Date posted
    5. Job category/department
    6. Job description (if available on the listing page)
    7. Job URL
    
    IMPORTANT: For any field that is not available or cannot be found, please explicitly include the field with a value of "N/A" rather than omitting it. Every job listing should have all seven fields listed above, even if some contain "N/A" values.
    
    If there are multiple pages of results, navigate through up to the first 5 jobs.
    
    Return the data as a structured list of job objects.
"""

def run_scraper():
    """
    Run the scraper and return the results
    
    Returns:
    - dict: The scraped job data
    """
    # Define the configuration using environment variables
    graph_config = {
        "llm": {
            "model": os.getenv("LLM_MODEL", "google_genai/gemini-2.0-flash"),
            "api_key": os.getenv("GOOGLE_API_KEY")
        },
        "verbose": os.getenv("VERBOSE", "True").lower() == "true",
        "headless": os.getenv("HEADLESS", "True").lower() == "true",
    }
    
    # URL to scrape
    source_url = os.getenv("SOURCE_URL", "https://www.google.com/about/careers/applications/jobs/results/")
    
    # Create the SmartScraperGraph instance
    smart_scraper_graph = SmartScraperGraph(
        prompt=SCRAPER_INSTRUCTIONS,       
        source=source_url,
        config=graph_config
    )
    
    # Run the pipeline
    return smart_scraper_graph.run()