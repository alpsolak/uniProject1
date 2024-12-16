import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import turtle

EXPENSES_FILE = "expenses.txt"
BUDGET_FILE = "budget.txt"
SCALE = 0.3  # Scale for the bar chart


# File handling functions
def load_file(file):
    try:
        with open(file, "r") as f:
            result = []
            for line in f.readlines():
                result.append(line.strip().split("\t"))
            return result
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file} not found.")
        return []


def save_expense(expense):
    with open(EXPENSES_FILE, "a") as f:
        f.write("\t".join(expense) + "\n")


def check_date(date_text):
    try:
        input_date = datetime.strptime(date_text, '%Y-%m-%d').date()  # Convert the date to a date object
        if input_date > datetime.today().date():  # Check if the date is in the future
            return False
        return True
    except ValueError:
        return False


# Add Expense Function
def add_expenses_window():
    def save_and_close():
        date = date_entry.get()
        amount = amount_entry.get()
        category = category_var.get()
        description = description_entry.get()

        if not check_date(date):
            messagebox.showerror("Error", "Invalid date. Use YYYY-MM-DD.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid amount.")
            return

        save_expense([date, str(amount), category, description])
        messagebox.showinfo("Success", "Expense added successfully!")
        window.destroy()

    window = tk.Toplevel()
    window.title("Add Expense")
    window.geometry("350x350")
    categories = ["Food", "Housing", "Transportation", "Education", "Entertainment", "Shopping", "Other"]

    tk.Label(window, text="Add New Expense", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(window, text="Date (YYYY-MM-DD):").pack()
    date_entry = tk.Entry(window)
    date_entry.pack(pady=5)

    tk.Label(window, text="Amount:").pack()
    amount_entry = tk.Entry(window)
    amount_entry.pack(pady=5)

    tk.Label(window, text="Category:").pack()
    category_var = tk.StringVar(value=categories[6])
    tk.OptionMenu(window, category_var, *categories).pack(pady=5)

    tk.Label(window, text="Description:").pack()
    description_entry = tk.Entry(window)
    description_entry.pack(pady=5)

    tk.Button(window, text="Save", command=save_and_close).pack(pady=20)


# View Expenses
def view_expenses_window():
    expenses = load_file(EXPENSES_FILE)

    window = tk.Toplevel()
    window.title("View Expenses")
    window.geometry("600x400")

    tk.Label(window, text="Expenses", font=("Arial", 14, "bold")).pack(pady=10)

    categories = ["All", "Food", "Housing", "Transportation", "Education", "Entertainment", "Shopping", "Other"]

    category_var = tk.StringVar(value="All")
    category_menu = tk.OptionMenu(window, category_var, *categories)
    category_menu.pack(pady=5)

    def update_treeview():
        for item in tree.get_children():
            tree.delete(item)

        selected_category = category_var.get()
        if selected_category == "All":
            filtered_expenses = expenses
        else:
            filtered_expenses = []
            for expense in expenses:
                if expense[2] == selected_category:
                    filtered_expenses.append(expense)

        for expense in filtered_expenses:
            tree.insert("", "end", values=expense)

    category_var.trace_add("write", lambda *args: update_treeview())

    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scroll_y = tk.Scrollbar(frame, orient="vertical")

    tree = ttk.Treeview(
        frame,
        columns=("Date", "Amount", "Category", "Description"),
        show="headings",
        yscrollcommand=scroll_y.set,
    )
    tree.heading("Date", text="Date")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")

    tree.column("Date", width=80, stretch=False)
    tree.column("Amount", width=100, anchor="e", stretch=False)
    tree.column("Category", width=130, anchor="center", stretch=False)
    tree.column("Description", width=200)

    scroll_y.config(command=tree.yview)

    scroll_y.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)

    update_treeview()

    window.mainloop()


# Bar Chart
def bar_chart_window():
    expenses = load_file(EXPENSES_FILE)
    categories = {"Food": 0, "Housing": 0, "Transportation": 0, "Education": 0,
                  "Entertainment": 0, "Shopping": 0, "Other": 0}

    for expense in expenses:
        categories[expense[2]] += float(expense[1])

    # Start drawing the bar chart
    wn = turtle.Screen()
    wn.bgcolor("white")
    wn.title("Expense Bar Chart")
    wn.setup(width=800, height=500)

    alex = turtle.Turtle()
    wn.tracer(0)
    alex.pensize(2)

    # Draw the chart axes
    alex.penup()
    alex.goto(-350, -200)  # Starting point
    alex.pendown()
    alex.forward(750)  # X axis
    alex.backward(750)
    alex.left(90)
    alex.forward(450)  # Y axis
    alex.backward(450)
    alex.right(90)

    # Draw the bars
    x_position = -300
    bar_width = 50
    colors = ["red", "blue", "green", "orange", "purple", "yellow", "cyan"]

    for i, (category, amount) in enumerate(categories.items()):
        alex.penup()
        alex.goto(x_position, -200)  # Base of the bar
        alex.pendown()
        alex.fillcolor(colors[i % len(colors)])
        alex.begin_fill()

        alex.left(90)
        alex.forward(amount * SCALE)  # Height of the bar
        alex.right(90)
        alex.forward(bar_width)
        alex.right(90)
        alex.forward(amount * SCALE)
        alex.left(90)
        alex.end_fill()

        # Write the category name below the bar
        alex.penup()
        alex.goto(x_position + bar_width / 2, -220)  # Position of category name
        alex.write(category, align="center", font=("Arial", 10, "normal"))

        # Write the expense amount on top of the bar
        alex.goto(x_position + bar_width / 2, -200 + amount * SCALE + 10)
        alex.write(f"${round(amount, 2)}", align="center", font=("Arial", 10, "normal"))

        x_position += bar_width + 50  # Position of the next bar
    alex.hideturtle()
    wn.update()
    wn.mainloop()


# Search Expenses
def search_expenses_window():
    expenses = load_file(EXPENSES_FILE)

    def update_treeview():
        for item in tree.get_children():
            tree.delete(item)
        key = search_entry.get().lower()
        for expense in expenses:
            if key in expense[3].lower() or key == expense[2].lower():
                tree.insert("", "end", values=expense)
    window = tk.Toplevel()
    window.title("Search Expenses")
    window.geometry("600x400")

    tk.Label(window, text="Search Expenses", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Enter word to search").pack()
    search_entry = tk.Entry(window)
    search_entry.pack(pady=5)
    tk.Button(window, text="Search", command=update_treeview).pack(pady=20)
    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scroll_y = tk.Scrollbar(frame, orient="vertical")

    tree = ttk.Treeview(
        frame,
        columns=("Date", "Amount", "Category", "Description"),
        show="headings",
        yscrollcommand=scroll_y.set,
    )
    tree.heading("Date", text="Date")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")

    tree.column("Date", width=80, stretch=False)
    tree.column("Amount", width=100, anchor="e", stretch=False)
    tree.column("Category", width=130, anchor="center", stretch=False)
    tree.column("Description", width=200)

    scroll_y.config(command=tree.yview)

    scroll_y.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)

    window.mainloop()


# Budget Alerts
def budget_alerts_window():
    expenses = load_file(EXPENSES_FILE)
    budget = load_file(BUDGET_FILE)
    total = {"Food": 0, "Housing": 0, "Transportation": 0, "Education": 0,
             "Entertainment": 0, "Shopping": 0, "Other": 0}

    for expense in expenses:
        total[expense[2]] += float(expense[1])

    window = tk.Toplevel()
    window.title("Budget Alerts")
    window.geometry("550x300")

    tk.Label(window, text="Budget Alerts", font=("Arial", 16, "bold")).pack()

    canvas = tk.Canvas(window, bg="white", width=500, height=220, highlightthickness=0)
    canvas.pack(pady=20)

    y_offset = 20
    for item in budget:
        category, limit = item[0], float(item[1])
        spent = total[category]
        if spent > limit:
            color = "red"
            text = f"{category}: OVER budget by {round(spent - limit, 2)}"
        else:
            color = "green"
            text = f"{category}: UNDER budget, remaining {round(limit - spent, 2)}"

        canvas.create_text(20, y_offset, anchor="w", text=text, fill=color, font=("Arial", 12, "bold"))
        y_offset += 30


# Main Menu
def main_menu():
    menu = tk.Tk()
    menu.title("Expense Manager")
    menu.geometry("400x400")

    tk.Label(menu, text="Expense Manager", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(menu, text="Add Expenses", width=20, command=add_expenses_window).pack(pady=10)
    tk.Button(menu, text="View Expenses", width=20, command=view_expenses_window).pack(pady=10)
    tk.Button(menu, text="Bar Chart", width=20, command=bar_chart_window).pack(pady=10)
    tk.Button(menu, text="Search Expenses", width=20, command=search_expenses_window).pack(pady=10)
    tk.Button(menu, text="Budget Alerts", width=20, command=budget_alerts_window).pack(pady=10)
    tk.Button(menu, text="Exit", width=20, command=menu.destroy).pack(pady=10)

    menu.mainloop()


main_menu()
