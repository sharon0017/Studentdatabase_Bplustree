import tkinter as tk
from tkinter import messagebox, scrolledtext
from student_record import StudentRecord, DatabaseException
from bplus_tree import BPlusTreeEngine

class StudentDBApp:
    def __init__(self, root):
        self.db = BPlusTreeEngine(order=4)
        self.root = root
        self.root.title("B+ Tree Student Database System")
        self.root.geometry("700x600")
        
        # Pre-populate some data for the live demo
        self._populate_sample_data()

        self.create_widgets()

    def _populate_sample_data(self):
        samples = [
            (1001, "Alice Smith", 3.85, "CSE", 2024),
            (1005, "Bob Johnson", 3.40, "ECE", 2023),
            (1010, "Charlie Brown", 3.92, "CSE", 2024),
            (1003, "David Miller", 2.95, "MECH", 2024)
        ]
        for sid, name, gpa, dept, year in samples:
            self.db.insert(StudentRecord(sid, name, gpa, dept, year))

    def create_widgets(self):
        # Insert Frame
        insert_frame = tk.LabelFrame(self.root, text="Insert New Record", padx=10, pady=10)
        insert_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(insert_frame, text="ID:").grid(row=0, column=0)
        self.ent_id = tk.Entry(insert_frame, width=10)
        self.ent_id.grid(row=0, column=1)

        tk.Label(insert_frame, text="Name:").grid(row=0, column=2)
        self.ent_name = tk.Entry(insert_frame, width=15)
        self.ent_name.grid(row=0, column=3)

        tk.Label(insert_frame, text="GPA:").grid(row=0, column=4)
        self.ent_gpa = tk.Entry(insert_frame, width=6)
        self.ent_gpa.grid(row=0, column=5)

        tk.Label(insert_frame, text="Dept:").grid(row=1, column=0)
        self.ent_dept = tk.Entry(insert_frame, width=10)
        self.ent_dept.grid(row=1, column=1)

        tk.Label(insert_frame, text="Year:").grid(row=1, column=2)
        self.ent_year = tk.Entry(insert_frame, width=10)
        self.ent_year.grid(row=1, column=3)

        tk.Button(insert_frame, text="Insert Record", command=self.insert_record, bg="lightblue").grid(row=1, column=4, columnspan=2, pady=5)

        # Search Frame
        search_frame = tk.LabelFrame(self.root, text="Point Search [ O(log N) ]", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(search_frame, text="Target ID:").grid(row=0, column=0)
        self.ent_search_id = tk.Entry(search_frame, width=15)
        self.ent_search_id.grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_record).grid(row=0, column=2)

        # Range Query Frame
        range_frame = tk.LabelFrame(self.root, text="Range Query [ O(log N + K) ]", padx=10, pady=10)
        range_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(range_frame, text="Start ID:").grid(row=0, column=0)
        self.ent_start_id = tk.Entry(range_frame, width=10)
        self.ent_start_id.grid(row=0, column=1)

        tk.Label(range_frame, text="End ID:").grid(row=0, column=2)
        self.ent_end_id = tk.Entry(range_frame, width=10)
        self.ent_end_id.grid(row=0, column=3)
        tk.Button(range_frame, text="Execute Scan", command=self.range_query).grid(row=0, column=4, padx=10)

        # Output Area
        output_frame = tk.LabelFrame(self.root, text="Database Output & Telemetry", padx=10, pady=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_output = scrolledtext.ScrolledText(output_frame, height=15, state='disabled', bg="black", fg="lightgreen")
        self.txt_output.pack(fill="both", expand=True)

        self.log_message("System Initialized. Pre-populated with 4 sample records.\n")

    def log_message(self, message):
        self.txt_output.config(state='normal')
        self.txt_output.insert(tk.END, message + "\n")
        self.txt_output.see(tk.END)
        self.txt_output.config(state='disabled')

    def insert_record(self):
        try:
            sid = int(self.ent_id.get())
            name = self.ent_name.get()
            gpa = float(self.ent_gpa.get())
            dept = self.ent_dept.get()
            year = int(self.ent_year.get())

            record = StudentRecord(sid, name, gpa, dept, year)
            self.db.insert(record)
            self.log_message(f"[INSERT SUCCESS] Added: {name} (ID: {sid})")
            
            # Clear inputs
            for ent in (self.ent_id, self.ent_name, self.ent_gpa, self.ent_dept, self.ent_year):
                ent.delete(0, tk.END)
                
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure numeric fields (ID, GPA, Year) contain valid numbers.")
        except DatabaseException as e:
            messagebox.showerror("Database Error", str(e))

    def search_record(self):
        try:
            sid = int(self.ent_search_id.get())
            record = self.db.search(sid)
            self.log_message(f"\n[MATCH FOUND] {record}")
            self.log_message(f"--> Telemetry: Node Accesses: {self.db.node_access_count} | Comparisons: {self.db.key_comparison_count}")
        except ValueError:
            messagebox.showerror("Input Error", "ID must be a number.")
        except DatabaseException as e:
            self.log_message(f"\n[SEARCH FAILED] {e}")

    def range_query(self):
        try:
            start_id = int(self.ent_start_id.get())
            end_id = int(self.ent_end_id.get())
            results = self.db.range_query(start_id, end_id)
            
            self.log_message(f"\n[RANGE SCAN] Found {len(results)} records in range [{start_id}, {end_id}]:")
            for rec in results:
                self.log_message(f" - {rec}")
            self.log_message(f"--> Telemetry: Leaf Steps: {self.db.node_access_count} | Comparisons: {self.db.key_comparison_count}")
        except ValueError:
            messagebox.showerror("Input Error", "IDs must be numbers.")
        except DatabaseException as e:
            self.log_message(f"\n[QUERY ERROR] {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDBApp(root)
    root.mainloop()