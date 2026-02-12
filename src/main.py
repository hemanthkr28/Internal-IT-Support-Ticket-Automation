from ticket_processor import (
    load_input_file,
    process_ticket_batch,
    save_output_files
)
import pandas as pd


def print_console_report(all_tickets, processed, rejected):

    print("\n--- SUMMARY REPORT ---")
    print(f"Total Tickets Received: {len(all_tickets)}")
    print(f"Successfully Processed: {len(processed)}")
    print(f"Rejected/Duplicates: {len(rejected)}")

    print("\n--- PROCESSED TICKETS ---")

    if processed:
        df = pd.DataFrame(processed)[
            ["ticket_id", "email", "assigned_department", "sla_deadline"]
        ]
        print(df.to_string(index=False))
    else:
        print("No processed tickets.")

    print("\n--- REJECTED TICKETS ---")

    if rejected:
        for ticket in rejected:
            print(
                f"ID: {ticket.get('ticket_id', 'N/A')} | "
                f"Reason: {ticket.get('error')}"
            )
    else:
        print("No rejected tickets.")


def run_ticket_automation():

    print("Loading input tickets...")
    tickets = load_input_file("data/input_tickets.csv")

    print("Processing tickets...")
    processed, rejected = process_ticket_batch(tickets)

    print("Saving output files...")
    save_output_files(processed, rejected)

    print_console_report(tickets, processed, rejected)

    print("\n Automation completed successfully!")



if __name__ == "__main__":
    run_ticket_automation()
