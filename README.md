📌 Internal IT Ticket Automation System
📖 Project Overview

The Internal IT Ticket Automation System is a Python-based automation tool designed to process IT support tickets efficiently.

The system reads ticket data from a CSV file, validates it, removes duplicates, assigns departments automatically, calculates SLA deadlines, and generates structured output reports.

This project simulates a real-world IT helpdesk ticket processing workflow.

🚀 Features

✅ Read ticket data from CSV file

✅ Email & Priority validation

✅ Data normalization (cleaning)

✅ Duplicate detection within 24 hours

✅ Automatic Ticket ID generation

✅ Department auto-assignment

✅ SLA deadline calculation

✅ Processed & Rejected ticket reports

✅ Console summary report

🏗️ Project Structure
it_ticket_automation/
│
├── data/
│   └── input_tickets.csv
│
├── output/
│   ├── processed_tickets.csv
│   └── rejected_tickets.csv
│
├── src/
│   ├── main.py
│   ├── ticket_processor.py
│   └── config.py
│
└── README.md

⚙️ How It Works
1️⃣ Input Stage

The system reads ticket data from input_tickets.csv.

Each row represents one ticket.

2️⃣ Processing Stage

Each ticket goes through:

Data normalization

Email validation (Regex)

Priority validation

Duplicate checking (within 24 hours)

Ticket ID generation (if missing)

Department assignment

SLA deadline calculation

3️⃣ Output Stage

The system generates:

processed_tickets.csv

rejected_tickets.csv

It also prints a summary report in the console.

🧠 Business Logic
🔹 SLA Rules

High → 4 hours

Medium → 8 hours

Low → 24 hours

🔹 Department Routing

WiFi → Network Team

Hardware → IT Support

Software → Application Team

▶️ How to Run the Project
Step 1: Install Dependencies
pip install pandas

Step 2: Run the Application
python src/main.py

📊 Sample Console Output
--- SUMMARY REPORT ---
Total Tickets Received: 10
Successfully Processed: 7
Rejected/Duplicates: 3

🛠️ Technologies Used

Python 3

Pandas

Regex

UUID

Datetime module

🎯 Design Principles

Separation of configuration and logic (config.py)

Clean data processing workflow

Modular structure

Scalable and maintainable design

📌 Future Enhancements

Database integration

REST API support

Web-based dashboard

Email notification system
