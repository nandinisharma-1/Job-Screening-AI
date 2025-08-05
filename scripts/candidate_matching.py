import sqlite3
import pandas as pd
import pdfplumber
import re
import os

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def load_job_descriptions(conn):
    """Loads job descriptions from the database."""
    query = "SELECT * FROM job_descriptions"
    return pd.read_sql_query(query, conn)

def extract_text_from_cv(cv_file):
    """Extracts text from a CV (PDF file)."""
    extracted_text = ""
    try:
        with pdfplumber.open(cv_file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from CV {cv_file}: {e}")
    
    return extracted_text.strip()

def extract_job_description_from_cv(cv_text):
    """Extracts the job description from the CV text."""
    job_description_match = re.search(r'Work Experience\s*(.*?)(?=Skills:|Certifications:|Achievements:|$)', cv_text, re.DOTALL)
    if job_description_match:
        return job_description_match.group(1).strip()
    return ""

def extract_job_title_from_cv(cv_text):
    """Extracts the job title from the CV text."""
    job_title_match = re.search(r'Work Experience\s*(.*?)\s+at', cv_text, re.DOTALL)
    if job_title_match:
        return job_title_match.group(1).strip()
    return ""

def match_candidate(cv_file, job):
    """Calculates the matching score for a candidate's CV against a job description."""
    cv_text = extract_text_from_cv(cv_file)
    job_title_from_cv = extract_job_title_from_cv(cv_text)

    if job_title_from_cv.lower() != job['title'].lower():
        return 0  # No match if job titles do not match

    job_description_from_cv = extract_job_description_from_cv(cv_text)
    job_description = job['description'].lower()
    cv_text_lower = job_description_from_cv.lower()

    keywords = re.findall(r'\b\w+\b', job_description)
    score = sum(1 for keyword in keywords if keyword in cv_text_lower)

    return score

def main():
    database = r"C:\Users\Nandini\Desktop\Job Screening AI\data\recruitment.db"
    cv_directory = r"C:\Users\Nandini\Desktop\Job Screening AI\data\cv"

    conn = create_connection(database)

    if conn:
        job_descriptions = load_job_descriptions(conn)

        for index, job in job_descriptions.iterrows():
            job_title = job['title']
            
            for cv_file in os.listdir(cv_directory):
                if cv_file.endswith('.pdf'):
                    cv_path = os.path.join(cv_directory, cv_file)
                    matching_score = match_candidate(cv_path, job)
                    
                    candidate_name = cv_file[:-4]  # Assuming the file name is the candidate's name
                    
                    if matching_score > 0:
                        print(f"Candidate: {candidate_name} | Job Title: {job_title} | Matching Score: {matching_score}")

        conn.close()
    else:
        print("Failed to create a database connection.")

if __name__ == "__main__":
    main()