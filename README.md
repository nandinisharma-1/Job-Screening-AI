
## Overview

The recruitment process often involves manually reviewing numerous job descriptions (JDs) and CVs, 
which can be time-consuming and prone to human error. The goal of this project is to develop a 
multi-agentic AI system that can automatically read and summarize job descriptions (JDs), match 
candidate qualifications with the JD, shortlist candidates, and send interview requests based on the 
match .

The JOB SCREENING AI is a multi-agent AI application designed to streamline the recruitment process. It automates the tasks of summarizing job descriptions, extracting data from CVs, matching candidates with job requirements, shortlisting candidates, and sending interview requests.

## Features

- **Job Description Summarization**: Automatically summarizes job descriptions using an on-premises large language model (LLM) via Ollama.
- **CV Data Extraction**: Extracts relevant information from candidate CVs in PDF format.
- **Candidate Matching**: Compares candidate qualifications with job descriptions and calculates match scores.
- **Shortlisting Candidates**: Shortlists candidates based on a defined match score threshold.
- **Interview Scheduling**: Sends personalized email invitations to shortlisted candidates with interview details.
- **Web Interface**: Provides a user-friendly web interface for interaction.


## Requirements

- Python 3.x
- Ollama (for on-premises LLMs)
- SQLite (for database management)
- Flask
- pandas
- smtplib
- email
- pdfplumber (for extracting text from CV PDFs)


## Project Structure

<img width="231" alt="overview" src="https://github.com/user-attachments/assets/f60fe804-3780-4df5-b632-7d2df800a97e" />





  ## Working of project 

<img width="393" alt="Project image" src="https://github.com/user-attachments/assets/78b311a4-b5b9-49b8-af88-79cb8ed3431e" />

1. Choose a CSV file of Job description and click on submit job description button.It will show summarize Job Description.


<img width="798" alt="ss 2" src="https://github.com/user-attachments/assets/ac55bcc1-8158-4e2e-996f-373831ad053a" />


<img width="959" alt="ss3" src="https://github.com/user-attachments/assets/e12e35a3-3484-40aa-9b01-4baa24244bb9" />



2.Now add number of CV from CV folder and click on Match candidate button.It will show the Name with job title and match score.

<img width="620" alt="score table" src="https://github.com/user-attachments/assets/f69c54c7-8f51-408c-b112-b1ad9f13f099" />


3.Based on above match score, candidates having score more than a threshold value (in this it is 50),a shorlisted candidates table generate.

4.For shortlisted candidates Interview get schedule with Date and time and email send for those shortlisted candidates for interview.

<img width="953" alt="shortlisted and interview" src="https://github.com/user-attachments/assets/16305402-3f8b-44d4-88b8-ffb68e7fedf3" />



## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd recruitment-automation

2. pip install -r requirements.txt                 #install the required packages


3. python scripts/database_setup.py                # Set up the SQLite database

4. python scripts/main.py                          #Run the Flask application

5. Open your web browser and navigate to ***link*** to access the application.




