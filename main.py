"""
File 4: main.py
Description: Main application execution loop with robust user input exception handling.
"""

from student_record import (
    StudentRecord, DatabaseException, DuplicateKeyException,
    RecordNotFoundException, InvalidRecordException, InvalidQueryRangeException
)
from bplus_tree import BPlusTreeEngine


def print_menu():
    print("\n=== STUDENT DATABASE MANAGEMENT SYSTEM (B+ TREE) ===")
    print("1. Insert New Student Record")
    print("2. Search Student by ID (Point Search)")
    print("3. Execute ID Range Query")
    print("4. Display B+ Tree Hierarchy Visualizer")
    print("5. Load Pre-Populated Benchmark Test Suite")
    print("6. Exit")


def get_int_input(prompt: str) -> int:
    """Helper method to handle integer input parsing exceptions."""
    while True:
        try:
            val = input(prompt).strip()
            return int(val)
        except ValueError:
            print("Input Error: Please enter a valid integer numeric value.")


def get_float_input(prompt: str) -> float:
    """Helper method to handle float input parsing exceptions."""
    while True:
        try:
            val = input(prompt).strip()
            return float(val)
        except ValueError:
            print("Input Error: Please enter a valid decimal number (e.g., 3.75).")


def main():
    db = BPlusTreeEngine(order=4)  # B+ Tree of order 4 (Max 3 keys per node)

    while True:
        print_menu()
        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            print("\n--- Insert Student Record ---")
            try:
                sid = get_int_input("Enter Student ID: ")
                name = input("Enter Student Name: ")
                gpa = get_float_input("Enter GPA (0.0 - 4.0): ")
                dept = input("Enter Department: ")
                year = get_int_input("Enter Enrollment Year: ")

                record = StudentRecord(sid, name, gpa, dept, year)
                db.insert(record)
                print("Record inserted successfully!")

            except (InvalidRecordException, DuplicateKeyException) as e:
                print(f"\n[INSERT REJECTED]: {e}")
            except DatabaseException as e:
                print(f"\n[DATABASE ERROR]: {e}")

        elif choice == "2":
            print("\n--- Point Search ---")
            try:
                sid = get_int_input("Enter Target Student ID: ")
                matched_record = db.search(sid)
                print("\n[MATCH FOUND]:")
                matched_record.display()
                print(f"Telemetry Metrics -> Node Accesses: {db.node_access_count} | Key Comparisons: {db.key_comparison_count}")

            except RecordNotFoundException as e:
                print(f"\n[SEARCH FAILED]: {e}")
            except DatabaseException as e:
                print(f"\n[DATABASE ERROR]: {e}")

        elif choice == "3":
            print("\n--- Range Query ---")
            try:
                start_id = get_int_input("Enter Start Student ID: ")
                end_id = get_int_input("Enter End Student ID: ")

                results = db.range_query(start_id, end_id)
                print(f"\nFound {len(results)} student record(s) in range [{start_id}, {end_id}]:")
                for rec in results:
                    rec.display()
                print(f"Telemetry Metrics -> Leaf Accesses: {db.node_access_count} | Key Comparisons: {db.key_comparison_count}")

            except InvalidQueryRangeException as e:
                print(f"\n[QUERY FAILED]: {e}")
            except DatabaseException as e:
                print(f"\n[DATABASE ERROR]: {e}")

        elif choice == "4":
            db.display_tree()

        elif choice == "5":
            print("\n--- Pre-populating Dataset ---")
            sample_dataset = [
                (1001, "Alice Smith", 3.85, "CSE", 2024),
                (1005, "Bob Johnson", 3.40, "ECE", 2023),
                (1010, "Charlie Brown", 3.92, "CSE", 2024),
                (1003, "David Miller", 2.95, "MECH", 2024),
                (1012, "Emma Watson", 3.78, "EEE", 2023),
                (1008, "Frank Wright", 3.10, "CIVIL", 2022),
                (1015, "Grace Hopper", 4.00, "CSE", 2021),
                (1002, "Hank Pym", 3.25, "ECE", 2023)
            ]

            inserted_count = 0
            for sid, name, gpa, dept, year in sample_dataset:
                try:
                    rec = StudentRecord(sid, name, gpa, dept, year)
                    db.insert(rec)
                    inserted_count += 1
                except DatabaseException as err:
                    print(f"Skipping record {sid}: {err}")

            print(f"Successfully populated {inserted_count} records.")

        elif choice == "6":
            print("Exiting Student Database System. Goodbye!")
            break
        else:
            print("Invalid menu choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()