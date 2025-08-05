# job_description_summarizer.py

import pandas as pd
from ollama_model import OllamaModel
import re
import sys
import io

# Set the encoding for standard output to UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Define the model name
model_name = "tinyllama:latest"  # Replace with the actual model name you are using

def summarize_job_description(job_description):
    """ 
    Summarizes the given job description using the TinyLlama model.

    Args:
        job_description (str): The job description text to summarize.

    Returns:
        str: The summarized text.
    """
    model = OllamaModel(model_name=model_name)
    return model.summarize(job_description)

def read_job_descriptions_from_csv(file_path):
    """ 
    Reads job descriptions from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of tuples containing job titles and descriptions.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path, encoding='latin1')  # or use encoding='cp1252'
        
        # Assuming the CSV has columns named 'Job Title' and 'Job Description'
        job_data = list(zip(df['Job Title'], df['Job Description']))
        
        # Clean and format job descriptions
        cleaned_job_data = []
        for title, description in job_data:
            cleaned_description = clean_job_description(description)
            cleaned_job_data.append((title, cleaned_description))
        
        return cleaned_job_data
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {str(e)}")
        return []

def clean_job_description(description):
    """ 
    Cleans the job description by removing unnecessary whitespace and formatting.

    Args:
        description (str): The raw job description text.

    Returns:
        str: The cleaned job description.
    """
    description = re.sub(r'\n+', '\n', description)  # Replace multiple newlines with a single newline
    description = re.sub(r'\s+', ' ', description)   # Replace multiple spaces with a single space
    description = description.strip()  # Remove leading and trailing whitespace

    return description

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = "C:\\Users\\Nandini\\Desktop\\Job Screening AI\\data\\job_description.csv"  # Update this path

    # Read job titles and descriptions from the CSV file
    job_data = read_job_descriptions_from_csv(csv_file_path)

    for job_title, description in job_data:
        print("Job Title:", job_title)
        summary = summarize_job_description(description)
        print("Summary:", summary)
        print("-" * 40)

    print("Summarization complete.")