import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import matplotlib.pyplot as plt
class Stack:
    def _init_(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return None

class ExpenseTrackerApp(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Expense Tracker")
        self.geometry("1300x600")
        self.configure(bg="light blue")
        self.expenses = Stack()
        self.categories = [
            "Food",
            "Transportation",
            "Utilities",
            "Entertainment",
            "Other",
        ]
        self.category_var = tk.StringVar(self)
        self.category_var.set(self.categories[0])
        self.currencies = ["USD", "EUR", "GBP", "JPY", "INR"]
        self.create_widgets()
        


    def create_widgets(self):
        label_style = {"font": ("Helvetica", 20, "bold"), "bg": "black", "fg": "white"}
        entry_style = {"font": ("Helvetica", 12), "bg": "black", "fg": "white", "insertbackground": "white"}
        button_style = {"font": ("Helvetica", 12), "bg": "white", "fg": "black"}

        self.label = tk.Label(
            self, text="Expense Tracker", font=("Helvetica", 20, "bold")
        )
        self.label.pack(pady=10)
        self.frame_input = tk.Frame(self)
        self.frame_input.pack(pady=10)
        self.expense_label = tk.Label(
            self.frame_input, text="Expense Amount:", font=("Helvetica", 12)
        )
        self.expense_label.grid(row=0, column=0, padx=5)
        self.expense_entry = tk.Entry(
            self.frame_input, font=("Helvetica", 12), width=15
        )
        self.expense_entry.grid(row=0, column=1, padx=5)
        self.item_label = tk.Label(
            self.frame_input, text="Item Description:", font=("Helvetica", 12)
        )
        self.item_label.grid(row=0, column=2, padx=5)
        self.item_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=20)
        self.item_entry.grid(row=0, column=3, padx=5)
        self.category_label = tk.Label(
            self.frame_input, text="Category:", font=("Helvetica", 12)
        )
        self.category_label.grid(row=0, column=4, padx=5)
        self.category_dropdown = ttk.Combobox(
            self.frame_input,
            textvariable=self.category_var,
            values=self.categories,
            font=("Helvetica", 12),
            width=15,
        )
        self.category_dropdown.grid(row=0, column=5, padx=5)
        self.date_label = tk.Label(
            self.frame_input, text="Date (YYYY-MM-DD):", font=("Helvetica", 12)
        )
        self.date_label.grid(row=0, column=6, padx=5)
        self.date_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=15)
        self.date_entry.grid(row=0, column=7, padx=5)
        self.add_button = tk.Button(self, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=5)
        self.frame_list = tk.Frame(self)
        self.frame_list.pack(pady=10)
        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_listbox = tk.Listbox(
            self.frame_list,
            font=("Helvetica", 12),
            width=70,
            yscrollcommand=self.scrollbar.set,
        )
        self.expense_listbox.pack(pady=5)
        self.scrollbar.config(command=self.expense_listbox.yview)
        
        self.delete_button = tk.Button(
            self, text="Delete Expense", command=self.delete_expense
        )
        self.delete_button.pack(pady=5)
        self.save_button = tk.Button(
            self, text="Save Expenses", command=self.save_expenses
        )
        self.save_button.pack(pady=5)
        self.total_label = tk.Label(
            self, text="Total Expenses:", font=("Helvetica", 12)
        )
        self.total_label.pack(pady=5)
        self.show_chart_button = tk.Button(
            self, text="Show Expenses Chart", command=self.show_expenses_chart
        )
        self.show_chart_button.pack(pady=5)
        self.update_total_label()

    def add_expense(self):
        expense = self.expense_entry.get()
        item = self.item_entry.get()
        category = self.category_var.get()
        date = self.date_entry.get()

        if expense and date:
            self.expenses.push((expense, item, category, date))
            self.refresh_list()
            self.expense_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Expense and Date cannot be empty.")

    def edit_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_expense = self.expenses[selected_index]
            new_expense = simpledialog.askstring(
                "Edit Expense", "Enter new expense:", initialvalue=selected_expense[0]
            )
            if new_expense:
                self.expenses[selected_index] = (
                    new_expense,
                    selected_expense[1],
                    selected_expense[2],
                    selected_expense[3],
                )
                self.refresh_list()
                self.update_total_label()

    def delete_expense(self):
        deleted_expense = self.expenses.pop()
        if deleted_expense:
            self.refresh_list()
            self.update_total_label()
        else:
            messagebox.showinfo("Info", "No expenses to delete.")

    def refresh_list(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.expenses.stack:
            self.expense_listbox.insert(
                tk.END, f"{expense[0]} - {expense[1]} - {expense[2]} ({expense[3]})"
            )

    def update_total_label(self):
        total_expenses = sum(float(expense[0]) for expense in self.expenses.stack)
        self.total_label.config(text=f"Total Expenses: INR {total_expenses:.2f}")
        
    def save_expenses(self):
        with open("expenses.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            column_headers = ["Expense Amount", "Item Description", "Category", "Date"]
            writer.writerow(column_headers)
            for expense in self.expenses:
                writer.writerow(expense)

    def show_expenses_chart(self):
        category_totals = {}
        for expense, _, category, _ in self.expenses.stack:
            try:
                amount = float(expense)
            except ValueError:
                continue
            category_totals[category] = category_totals.get(category, 0) + amount
        categories = list(category_totals.keys())
        expenses = list(category_totals.values())
        plt.figure(figsize=(8, 6))
        plt.pie(
            expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True
        )
        plt.axis("equal")
        plt.title(f"Expense Categories Distribution (INR)")
        plt.show()

    def show_expenses_chart(self):
        category_totals = {}
        for expense, _, category, _ in self.expenses.stack:
            try:
                amount = float(expense)
            except ValueError:
                continue
            category_totals[category] = category_totals.get(category, 0) + amount
        categories = list(category_totals.keys())
        expenses = list(category_totals.values())
        highest_category = categories[expenses.index(max(expenses))]
        plt.figure(figsize=(8, 6))
        plt.pie(expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True)
        plt.axis("equal")
        plt.title(f"Expense Categories Distribution (INR)")
        plt.show()
        if highest_category == "Food":
            messagebox.showinfo("Expense Warning", "You are spending way too much on food, please start eating in the mess!")
        elif highest_category == "Transportation":
            messagebox.showwarning("Expense Warning", "Your transportation expenses are high, please start walking on foot!")
        elif highest_category == "Utilities":
            messagebox.showwarning("Expense Warning", "Utilities expenses are high, please start budgeting sincerely!")
        elif highest_category == "Entertainment":
            messagebox.showwarning("Expense Warning", "Your entertainment expenses are high, please try to control them!")
        elif highest_category == "Other":
            messagebox.showwarning("Expense Warning", "Expenses in 'Other' category are high, please avoid miscallaneous expenses!")


        


if _name_ == "_main_":
    app = ExpenseTrackerApp()
    app.mainloop()