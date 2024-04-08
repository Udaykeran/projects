import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def validate_data():
    name = name_entry.get()
    aicte_id = aicte_id_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    college = college_entry.get()

    # Basic validation
    if not all([name, aicte_id, email, phone, college]):
        messagebox.showerror("Error", "All fields are required.")
        return

    if not name_valid(name):
        messagebox.showerror("Error", "Name should not contain numbers.")
        return

    if not email_valid(email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    if not phone_valid(phone):
        messagebox.showerror("Error", "Invalid phone number format.")
        return

    generate_pdf(name, aicte_id, email, phone, college)
    messagebox.showinfo("Success", "PDF generated successfully.")

def name_valid(name):
    return not any(char.isdigit() for char in name)

def email_valid(email):
    
    return "@" in email and "." in email

def phone_valid(phone):
    
    return len(phone) == 10 and phone.isdigit()

def generate_pdf(name, aicte_id, email, phone, college):
    pdf_path = "candidate_details.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "Candidate Details")
    c.drawString(100, 730, f"Name: {name}")
    c.drawString(100, 710, f"AICTE ID: {aicte_id}")
    c.drawString(100, 690, f"Email: {email}")
    c.drawString(100, 670, f"Phone: {phone}")
    c.drawString(100, 650, f"College: {college}")
    c.save()

# GUI
m= tk.Tk()
m.title("Candidate Information")

tk.Label(m, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(m)
name_entry.grid(row=0, column=1)

tk.Label(m, text="AICTE ID:").grid(row=1, column=0)
aicte_id_entry = tk.Entry(m)
aicte_id_entry.grid(row=1, column=1)

tk.Label(m, text="Email:").grid(row=2, column=0)
email_entry = tk.Entry(m)
email_entry.grid(row=2, column=1)

tk.Label(m, text="Phone:").grid(row=3, column=0)
phone_entry = tk.Entry(m)
phone_entry.grid(row=3, column=1)

tk.Label(m, text="College:").grid(row=4, column=0)
college_entry= tk.Entry(m)
college_entry.grid(row=4, column=1)

submit = tk.Button(m, text="Submit", command=validate_data)
submit.grid(row=5, column=0, columnspan=2)

m.mainloop()
