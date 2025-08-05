import sqlite3
import csv
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

def insert_job_description(conn, title, description):
    """Insert a new job description into the job_descriptions table."""
    sql = '''INSERT INTO job_descriptions(title, description)
             VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (title, description))
    conn.commit()
    return cur.lastrowid

def parse_description(description):
    """Parse the job description to extract sections."""
    sections = {
        "Description": "",
        "Qualification": "",
        "Responsibilities": ""
    }
    
    # Use regex to find sections
    description_match = re.search(r'Description:\s*(.*?)(?=Qualification:|Responsibilities:|$)', description, re.DOTALL)
    qualification_match = re.search(r'Qualification:\s*(.*?)(?=Responsibilities:|$)', description, re.DOTALL)
    responsibilities_match = re.search(r'Responsibilities:\s*(.*?)(?=$)', description, re.DOTALL)

    if description_match:
        sections['Description'] = description_match.group(1).strip()
    if qualification_match:
        sections['Qualification'] = qualification_match.group(1).strip()
    if responsibilities_match:
        sections['Responsibilities'] = responsibilities_match.group(1).strip()

    # Combine sections back into a single description if needed
    combined_description = f"Description: {sections['Description']}\nQualification: {sections['Qualification']}\nResponsibilities: {sections['Responsibilities']}"
    
    return combined_description

def insert_job_descriptions_from_csv(conn, csv_file):
    """Insert job descriptions from a CSV file into the job_descriptions table."""
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if there is one
            for row in csv_reader:
                if len(row) >= 2:  # Ensure there are at least two columns
                    title = row[0].strip()
                    description = row[1].strip()

                    # Parse the description to extract sections
                    parsed_description = parse_description(description)

                    job_id = insert_job_description(conn, title, parsed_description)
                    print(f"Inserted job description with ID: {job_id}")
    except UnicodeDecodeError:
        print("UTF-8 decoding failed. Retrying with windows-1252 encoding...")
        with open(csv_file, mode='r', encoding='windows-1252') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if there is one
            for row in csv_reader:
                if len(row) >= 2:  # Ensure there are at least two columns
                    title = row[0].strip()
                    description = row[1].strip()

                    # Parse the description to extract sections
                    parsed_description = parse_description(description)

                    job_id = insert_job_description(conn, title, parsed_description)
                    print(f"Inserted job description with ID: {job_id}")


def main():
    database = r"C:\Users\Nandini\Desktop\Job Screening AI\data\recruitment.db"  # Path to your database file
    csv_file = r"C:\Users\Nandini\Desktop\Job Screening AI\data\job_description.csv"  # Path to your CSV file

    conn = create_connection(database)

    if conn:
        insert_job_descriptions_from_csv(conn, csv_file)
        conn.close()
    else:
        print("Failed to create a database connection.")

if __name__ == '__main__':
    main()