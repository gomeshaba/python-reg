import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1350x700+0+0")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Student Management System", bd=6, relief=tk.GROOVE,
                        font=("Algerian", 30, 'bold'), bg='dark blue', fg='white')
        title.pack(side=tk.TOP, fill=tk.X)

        # Variables for student data
        self.sl_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.batch_var = tk.StringVar()
        self.adate_var = tk.StringVar()
        self.mob_var = tk.StringVar()
        self.pmob_var = tk.StringVar()

        # Payment data
        self.pay_month_var = tk.StringVar()
        self.pay_amount_var = tk.StringVar()

        self.create_manage_frame()
        self.create_detail_frame()

    def create_manage_frame(self):
        manage_frame = tk.LabelFrame(self.root, bd=4, relief=tk.RIDGE, bg='light blue', text="Manage Students")
        manage_frame.place(x=15, y=80, width=460, height=580)

        # Add student entry fields
        entries = [
            ("Serial No", self.sl_var),
            ("Name", self.name_var),
            ("Class", self.class_var),
            ("Batch Name", self.batch_var),
            ("Amount paid", self.adate_var),
            ("Mobile", self.mob_var),
            ("Parents Mobile", self.pmob_var)
        ]

        for i, (label_text, var) in enumerate(entries):
            lbl = tk.Label(manage_frame, text=label_text, bg="light blue", fg="black", font=("times new roman", 14, 'bold'))
            lbl.grid(row=i, column=0, pady=10, padx=20, sticky='w')

            txt = tk.Entry(manage_frame, textvariable=var, font=('times new roman', 14), bd=2, relief=tk.GROOVE)
            txt.grid(row=i, column=1, pady=10, padx=20, sticky='w')

        # Add payment fields
        lbl_pay = tk.Label(manage_frame, text="Date of payment", bg="light blue", fg="black", font=("times new roman", 14, 'bold'))
        lbl_pay.grid(row=7, column=0)

        combo_pay = ttk.Combobox(manage_frame, width=14, textvariable=self.pay_month_var,
                                font=("times new roman", 12, 'bold'), state='readonly')
        combo_pay['values'] = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
        combo_pay.grid(row=7, column=1)

        txt_pay = tk.Entry(manage_frame, textvariable=self.pay_amount_var, width=5, font=('times new roman', 14), bd=2, relief=tk.GROOVE)
        txt_pay.grid(row=7, column=2)

        # Buttons
        btn_frame = tk.Frame(manage_frame, bd=4, relief=tk.RIDGE, bg='white')
        btn_frame.place(x=10, y=470, width=425)

        buttons = [
            ("Add", self.add_student),
            ("Update", self.update_data),
            ("Delete", self.delete_data),
            ("Clear", self.clear)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, width=10, command=command)
            btn.grid(row=0, column=i, padx=10, pady=10)

    def create_detail_frame(self):
        detail_frame = tk.LabelFrame(self.root, bd=4, relief=tk.RIDGE, bg='light blue', text="Student Details")
        detail_frame.place(x=500, y=80, width=820, height=580)

        # Search functionality
        lbl_search = tk.Label(detail_frame, text="Search By", bg="light blue", fg="black", font=("times new roman", 16, 'bold'))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky='w')

        self.search_by = tk.StringVar()
        combo_search = ttk.Combobox(detail_frame, width=10, textvariable=self.search_by, font=("times new roman", 12, 'bold'), state='readonly')
        combo_search['values'] = ("sl", "name", "class")
        combo_search.grid(row=0, column=1, pady=10, padx=20)

        self.search_txt = tk.StringVar()
        txt_search = tk.Entry(detail_frame, width=30, textvariable=self.search_txt, font=('times new roman', 14), bd=2, relief=tk.GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=20, sticky='w')

        searchbtn = tk.Button(detail_frame, text="Search", width=10, command=self.search_data)
        searchbtn.grid(row=0, column=3, padx=10, pady=10)

        showallbtn = tk.Button(detail_frame, text="Show All", width=10, command=self.fetch_data)
        showallbtn.grid(row=0, column=4, padx=10, pady=10)

        # Student data table
        table_frame = tk.Frame(detail_frame, bd=2, relief=tk.RIDGE, bg='light blue')
        table_frame.place(x=10, y=80, width=785, height=480)

        scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        self.student_table = ttk.Treeview(table_frame, columns=("sl", "name", "class", "batch", "adate", "mob", "pmob",
                                                                "jan", "feb", "mar", "apr", "may", "jun", "jul",
                                                                "aug", "sep", "oct", "nov", "dec"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        self.student_table.heading("sl", text="Sl.No")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("class", text="Class")
        self.student_table.heading("batch", text="Batch")
        self.student_table.heading("adate", text="Admit Date")
        self.student_table.heading("mob", text="Mobile")
        self.student_table.heading("pmob", text="Parents Mobile")

        self.student_table.heading("jan", text="January")
        self.student_table.heading("feb", text="February")
        self.student_table.heading("mar", text="March")
        self.student_table.heading("apr", text="April")
        self.student_table.heading("may", text="May")
        self.student_table.heading("jun", text="June")
        self.student_table.heading("jul", text="July")
        self.student_table.heading("aug", text="August")
        self.student_table.heading("sep", text="September")
        self.student_table.heading("oct", text="October")
        self.student_table.heading("nov", text="November")
        self.student_table.heading("dec", text="December")

        self.student_table['show'] = 'headings'

        for col in ("sl", "name", "class", "batch", "adate", "mob", "pmob", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"):
            self.student_table.column(col, width=100)

        self.student_table.pack(fill=tk.BOTH, expand=1)

    def add_student(self):
        try:
            conn = sqlite3.connect("student.db")
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS students (
                sl TEXT PRIMARY KEY,
                name TEXT,
                class TEXT,
                batch TEXT,
                adate TEXT,
                mob TEXT,
                pmob TEXT,
                jan TEXT,
                feb TEXT,
                mar TEXT,
                apr TEXT,
                may TEXT,
                jun TEXT,
                jul TEXT,
                aug TEXT,
                sep TEXT,
                oct TEXT,
                nov TEXT,
                dec TEXT
            )''')
            conn.commit()
            # Execute INSERT statement
            cur.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (self.sl_var.get(), self.name_var.get(), self.class_var.get(), self.batch_var.get(),
                         self.adate_var.get(), self.mob_var.get(), self.pmob_var.get(), "", "", "", "", "",
                         "", "", "", "", "", "", ""))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.clear()
            messagebox.showinfo("Success", "Record has been inserted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def fetch_data(self):
        try:
            conn = sqlite3.connect("student.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching data: {str(e)}")

    def clear(self):
        self.sl_var.set("")
        self.name_var.set("")
        self.class_var.set("")
        self.batch_var.set("")
        self.adate_var.set("")
        self.mob_var.set("")
        self.pmob_var.set("")
        self.pay_month_var.set("")
        self.pay_amount_var.set("")

    def search_data(self):
        try:
            conn = sqlite3.connect("student.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE " + str(self.search_by.get()) + " LIKE '%" + str(
                self.search_txt.get()) + "%'")
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while searching data: {str(e)}")

    def update_data(self):
        try:
            conn = sqlite3.connect("student.db")
            cur = conn.cursor()
            cur.execute("""UPDATE students SET name=?,class=?,batch=?,adate=?,mob=?,pmob=?,jan=?,
                        feb=?,mar=?,apr=?,may=?,jun=?,jul=?,aug=?,sep=?,oct=?,nov=?,dec=? WHERE sl=?""",
                        (self.name_var.get(),
                         self.class_var.get(),
                         self.batch_var.get(),
                         self.adate_var.get(),
                         self.mob_var.get(),
                         self.pmob_var.get(), "", "", "", "", "", "", "", "", "", "", "", "", int(self.sl_var.get())))

            conn.commit()
            self.fetch_data()
            self.clear()
            conn.close()
            messagebox.showinfo("Success", "Record has been updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating data: {str(e)}")

    def delete_data(self):
        try:
            conn = sqlite3.connect("student.db")
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE sl=?", (int(self.sl_var.get()),))
            conn.commit()
            self.fetch_data()
            self.clear()
            conn.close()
            messagebox.showinfo("Success", "Record has been deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting data: {str(e)}")


def main():
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
