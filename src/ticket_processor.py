import re
import uuid
from datetime import datetime, timedelta
import pandas as pd
from config import (
    SLA_TIME_HOURS,
    DEPARTMENT_ROUTING,
    VALID_PRIORITIES,
    EMAIL_PATTERN
)


def load_input_file(file_path):
    """Reads ticket CSV and converts to list of dictionaries"""
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")


def validate_email_address(email):
    return re.match(EMAIL_PATTERN, email)


def generate_ticket_id():
    return str(uuid.uuid4())[:8]


def process_ticket_batch(ticket_list):

    successful_tickets = []
    failed_tickets = []
    duplicate_check_log = []

    ticket_list.sort(
        key=lambda t: datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S")
    )

    for ticket in ticket_list:

        email = str(ticket.get("email", "")).strip().lower()
        issue = str(ticket.get("issue_type", "other")).strip().lower()
        priority = str(ticket.get("priority", "Low")).strip().capitalize()

        if not validate_email_address(email):
            ticket["error"] = "Invalid email format"
            failed_tickets.append(ticket)
            continue

        if priority not in VALID_PRIORITIES:
            ticket["error"] = "Invalid priority value"
            failed_tickets.append(ticket)
            continue

        current_time = datetime.strptime(
            ticket["timestamp"], "%Y-%m-%d %H:%M:%S")

        is_duplicate = False

        for past_record in duplicate_check_log:
            if (
                past_record["email"] == email
                and past_record["issue"] == issue
            ):
                hours_gap = (
                    current_time - past_record["time"]
                ).total_seconds() / 3600

                if hours_gap < 24:
                    is_duplicate = True
                    break

        if is_duplicate:
            ticket["error"] = "Duplicate ticket within 24 hours"
            failed_tickets.append(ticket)
            continue

        duplicate_check_log.append({
            "email": email,
            "issue": issue,
            "time": current_time
        })

        ticket_id = ticket.get("ticket_id")

        if not ticket_id or pd.isna(ticket_id):
            ticket_id = generate_ticket_id()

        assigned_department = DEPARTMENT_ROUTING.get(issue, "General")

        sla_deadline = current_time + timedelta(
            hours=SLA_TIME_HOURS[priority]
        )

        cleaned_ticket = {
            "ticket_id": ticket_id,
            "name": ticket.get("name"),
            "email": email,
            "issue_type": issue,
            "priority": priority,
            "assigned_department": assigned_department,
            "sla_deadline": sla_deadline.strftime("%Y-%m-%d %H:%M:%S"),
            "description": ticket.get("description")
        }

        successful_tickets.append(cleaned_ticket)

    return successful_tickets, failed_tickets


def save_output_files(processed, rejected):

    processed_df = pd.DataFrame(processed)
    rejected_df = pd.DataFrame(rejected)

    processed_df.to_csv("data/processed_tickets.csv", index=False)
    rejected_df.to_csv("data/rejected_tickets.csv", index=False)

    summary = {
        "Total Tickets": [len(processed) + len(rejected)],
        "Processed": [len(processed)],
        "Rejected": [len(rejected)]
    }

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv("data/summary_report.csv", index=False)

    
    if not processed_df.empty:
        team_summary = (
            processed_df["assigned_department"]
            .value_counts()
            .reset_index()
        )
        team_summary.columns = ["Department", "Ticket_Count"]
        team_summary.to_csv("data/team_summary.csv", index=False)
