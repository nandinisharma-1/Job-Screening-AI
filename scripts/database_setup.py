import sqlite3
import os
import pandas as pd

def create_connection():
    """Create a database connection to the SQLite database specified by db_file."""
    database = r"C:\Users\Nandini\Desktop\Job Screening AI\data\recruitment.db"
    conn = sqlite3.connect(database)
    return conn

def setup_database(conn):
    """Create tables if they do not exist."""
    cursor = conn.cursor()

    # Drop the candidates table if it exists (for development purposes)
    cursor.execute('DROP TABLE IF EXISTS candidates')

    # Create candidates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        skills TEXT
    )
    ''')

    # Create job_descriptions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')

    # Create interview_schedules table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interview_schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        job_id INTEGER,
        interview_date TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates (id),
        FOREIGN KEY (job_id) REFERENCES job_descriptions (id)
    )
    ''')

    conn.commit()

def insert_job_descriptions_from_csv(conn, csv_file):
    """Insert job descriptions from a CSV file into the job_descriptions table."""
    job_descriptions = pd.read_csv(csv_file, encoding='ISO-8859-1')  # Load job descriptions

    for index, row in job_descriptions.iterrows():
        title = row['Job Title']
        description = row['Job Description']
        
        # Insert into the database
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO job_descriptions (title, description)
            VALUES (?, ?)
        ''', (title, description))
    
    conn.commit()

def main():
    database = r"C:\Users\Nandini\Desktop\Job Screening AI\data\recruitment.db"
    
    # Check if the database already exists
    if not os.path.exists(database):
        conn = create_connection()
        setup_database(conn)
        conn.close()
        print("Database created and tables set up.")
    else:
        print("Database already exists.")
    
    # Insert job descriptions from CSV
    conn = create_connection()
    csv_file = r"C:\Users\Nandini\Desktop\Job Screening AI\data\job_description.csv"
    insert_job_descriptions_from_csv(conn, csv_file)
    conn.close()
    print("Job descriptions inserted into the database.")

if __name__ == "__main__":
    main()