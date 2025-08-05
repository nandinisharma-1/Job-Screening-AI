import pandas as pd
import os
from datetime import datetime, timedelta
import pdfplumber
import re

def extract_text_from_cv(cv_file):
    """
    Extracts text from a CV (PDF file).
    
    Args:
        cv_file (str): The CV file name.
    
    Returns:
        str: The extracted text from the CV.
    """
    extracted_text = ""
    try:
        with pdfplumber.open(cv_file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from CV {cv_file}: {e}")
    
    return extracted_text.strip()

def get_matching_score(cv_file, job):
    """
    Calculates the matching score for a candidate's CV against a job description.
    
    Args:
        cv_file (str): The CV file name.
        job (Series): A row from the job descriptions DataFrame.
    
    Returns:
        int: The matching score.
    """
    # Extract text from the CV
    cv_text = extract_text_from_cv(cv_file)

    # Extract job description sections
    job_description = job['Job Description'].lower()  # Assuming 'Job Description' is the column name
    cv_text_lower = cv_text.lower()

    # Calculate the matching score based on the number of keywords found in the CV
    keywords = re.findall(r'\b\w+\b', job_description)  # Extract words as keywords
    score = sum(1 for keyword in keywords if keyword in cv_text_lower)

    return score

def schedule_interviews(job_descriptions, cv_directory, threshold=60):
    """
    Schedules interviews for candidates based on matching scores.
    
    Args:
        job_descriptions (DataFrame): A DataFrame containing job descriptions.
        cv_directory (str): The directory containing CVs.
        threshold (int): The minimum matching score to schedule an interview.
    
    Returns:
        list: A list of scheduled interviews.
    """
    scheduled_interviews = []

    for index, job in job_descriptions.iterrows():
        job_title = job['Job Title']
        print(f"Scheduling interviews for job: {job_title}")
        
        for cv_file in os.listdir(cv_directory):
            if cv_file.endswith('.pdf'):
                candidate_name = cv_file[:-4]  # Assuming the file name is the candidate's name
                cv_path = os.path.join(cv_directory, cv_file)  # Get the full path to the CV
                matching_score = get_matching_score(cv_path, job)  # Call the updated function

                if matching_score >= threshold:  # Schedule for scores >= 20
                    # Schedule the interview for the candidate
                    interview_time = datetime.now() + timedelta(days=1)  # Schedule for 1 day later
                    scheduled_interviews.append({
                        'candidate_name': candidate_name,
                        'job_title': job_title,
                        'matching_score': matching_score,
                        'interview_time': interview_time.strftime("%Y-%m-%d %H:%M:%S")  # Format the date and time
                    })
                    print(f"Scheduled interview for {candidate_name} with score: {matching_score} at {interview_time.strftime('%Y-%m-%d %H:%M:%S')}")

    return scheduled_interviews

def main():
    job_description_path = r"C:\Users\Nandini\Desktop\Job Screening AI\data\job_description.csv"
    
    try:
        job_descriptions = pd.read_csv(job_description_path, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error loading job descriptions: {e}")
        return  # Exit if there's an error loading the CSV

    cv_directory = r"C:\Users\Nandini\Desktop\Job Screening AI\data\cv"
    
    scheduled_interviews = schedule_interviews(job_descriptions, cv_directory)

    # Output the scheduled interviews
    print("\nScheduled Interviews:")
    for interview in scheduled_interviews:
        print(f"Candidate: {interview['candidate_name']}, Job Title: {interview['job_title']}, Score: {interview['matching_score']}, Interview Time: {interview['interview_time']}")

if __name__ == "__main__":
    main()