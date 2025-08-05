import sqlite3
import pdfplumber
import os
import logging
import re

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Connection established.")
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
    return conn

def insert_candidate(conn, name, email, phone, skills):
    """Insert a new candidate into the candidates table."""
    sql = '''INSERT INTO candidates(name, email, phone, skills) VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (name, email, phone, skills))
    conn.commit()
    return cur.lastrowid

def extract_text_from_cv(pdf_path):
    """Extracts text from a CV (PDF file)."""
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        logging.error(f"Error extracting text from CV {pdf_path}: {e}")
    
    return extracted_text.strip()

def parse_cv_text(cv_text):
    """Parse the CV text to extract candidate information."""
    # Example regex patterns for extracting email, phone, and skills
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d[\d -]{8,}\d'  # Adjust this pattern based on expected phone formats
    skills_pattern = r'Skills:\s*(.*?)(?=\n|$)'  # Adjust based on your CV format

    email = re.search(email_pattern, cv_text)
    phone = re.search(phone_pattern, cv_text)
    skills = re.search(skills_pattern, cv_text)

    return {
        "email": email.group(0) if email else "N/A",
        "phone": phone.group(0) if phone else "N/A",
        "skills": skills.group(1).strip() if skills else "N/A"
    }

def process_cv_directory(cv_directory, conn):
    """Processes all CVs in the specified directory and inserts candidate data into the database."""
    for cv_file in os.listdir(cv_directory):
        if cv_file.endswith('.pdf'):
            cv_path = os.path.join(cv_directory, cv_file)
            cv_text = extract_text_from_cv(cv_path)

            # Parse the CV text to extract candidate information
            candidate_info = parse_cv_text(cv_text)
            name = cv_file[:-4]  # Assuming the file name is the candidate's name
            email = candidate_info['email']
            phone = candidate_info['phone']
            skills = candidate_info['skills']

            candidate_id = insert_candidate(conn, name, email, phone, skills)
            # Print the desired output
            print(f"Processing CV: {cv_file}")
            print(f"Inserted candidate with ID: {candidate_id}")

def main():
    database = r"C:\Users\Nandini\Desktop\Job Screening AI\data\recruitment.db"  # Path to your database file
    cv_directory = r"C:\Users\Nandini\Desktop\Job Screening AI\data\cv"  # Path to your CV directory

    conn = create_connection(database)

    if conn:
        process_cv_directory(cv_directory, conn)
        conn.close()
    else:
        logging.error("Failed to create a database connection.")

if __name__ == "__main__":
    main()