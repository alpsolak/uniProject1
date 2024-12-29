import tkinter as tk  # Import the tkinter module
from tkinter import ttk, messagebox  # Import the ttk and messagebox modules
from datetime import datetime  # Import the datetime module

EXPENSES_FILE = "expenses.txt"  # File to store the expenses
BUDGET_FILE = "budget.txt"  # File to store the budget
SCALE = 0.3  # Scale for the bar chart
FONT = "Arial"  # Font for the labels
categories = ["Food", "Housing", "Transportation", "Education", "Entertainment", "Shopping", "Other"]


# File handling functions
def load_file(file):
    # Load the file and return the contents
    try:
        with open(file, "r") as f:
            expenses = []
            # Read the file line by line and append to the expenses list
            for line in f:
                expenses.append(line.strip().split("\t"))
            return expenses
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file} not found.")
        if file == BUDGET_FILE:
            return [[i, 0] for i in categories]
        return []


def save_expense(expense):
    # Save the expense to the file
    with open(EXPENSES_FILE, "a") as f:
        f.write("\t".join(expense) + "\n")


# Sum the expenses by category
def sum_expenses():
    expenses = load_file(EXPENSES_FILE)
    total = {i[0]: 0 for i in budget}
    for expense in expenses:
        total[expense[2]] += float(expense[1])
    return total


# Create a new window
def create_window(title, geometry):
    window = tk.Toplevel()
    window.title(title)
    window.geometry(geometry)
    return window


# Create a frame for viewing expenses and search expenses
def create_frame(window):
    columns = ("Date", "Amount", "Category", "Description")
    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scroll_y = tk.Scrollbar(frame, orient="vertical")

    tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scroll_y.set)
    # Set the headings and columns
    for col in columns:
        tree.heading(col, text=col)

    tree.column("Date", width=80, stretch=False)
    tree.column("Amount", width=100, anchor="e", stretch=False)
    tree.column("Category", width=130, anchor="center", stretch=False)
    tree.column("Description", width=200)

    scroll_y.config(command=tree.yview)

    scroll_y.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)
    return tree


def check_date(date_text):
    # Check if the date is in the correct format and not in the future
    try:
        input_date = datetime.strptime(date_text, '%Y-%m-%d').date()  # Convert the date to a date object
        if input_date > datetime.today().date():  # Check if the date is in the future
            return False
        return True
    except ValueError:
        return False


# Add Expense Function
def add_expenses_window():
    # Function to save the expense and close the window
    def save_and_close():
        # Get the values from the entries
        date = date_entry.get().strip()
        amount = amount_entry.get().strip()
        category = category_var.get().strip()
        description = description_entry.get().strip()
        # Check if the values are valid
        if not check_date(date):
            messagebox.showerror("Error", "Invalid date. Use YYYY-MM-DD. Date cannot be in the future.")
            return
        try:
            amount = amount.replace(",", ".")
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid amount.")
            return
        if description == "":
            messagebox.showerror("Error", "Description cannot be empty.")
            return

        save_expense([date, str(amount), category, description])
        messagebox.showinfo("Success", "Expense added successfully!")
        window.destroy()

    window = create_window("Add Expense", "350x350")

    tk.Label(window, text="Add New Expense", font=(FONT, 14, "bold")).pack(pady=10)

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


# View Expenses Function
def view_expenses_window():
    expenses = load_file(EXPENSES_FILE)

    window = create_window("View Expenses", "600x400")

    tk.Label(window, text="Expenses", font=(FONT, 14, "bold")).pack(pady=10)

    # Function to update the treeview based on the selected category
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

        for i in filtered_expenses:
            tree.insert("", "end", values=i)

    category_var = tk.StringVar(value="All")
    # Create a frame for the filter
    filter_frame = tk.Frame(window)
    filter_frame.pack(pady=10)

    # Create the category menu and filter button
    tk.OptionMenu(filter_frame, category_var, *(categories + ["All"])).pack(side="left", padx=5)
    tk.Button(filter_frame, text="Filter", command=update_treeview).pack(side="left", padx=5)

    tree = create_frame(window)

    update_treeview()


# Bar Chart
def bar_chart_window():
    total = sum_expenses()
    window = create_window(" Expense Bar Chart", "700x500")
    # Create a canvas
    canvas = tk.Canvas(window, width=690, height=500)
    canvas.pack()
    # variables for the bar chart
    x_position = 50
    bar_width = 50
    colors = ["red", "blue", "green", "orange", "purple", "yellow", "cyan"]

    for i, (category, amount) in enumerate(total.items()):
        bar_height = amount * SCALE
        # Draw the bar
        canvas.create_rectangle(x_position, 450 - bar_height, x_position + bar_width, 450, fill=colors[i])
        # Add the category name below the bar
        canvas.create_text(x_position + bar_width / 2, 470, text=category, font=(FONT, 10))
        # Add the amount on top of the bar
        canvas.create_text(x_position + bar_width / 2, 450 - bar_height - 10,
                           text=f"₺{amount}", font=(FONT, 10))
        # Increase the x position for the next bar
        x_position += bar_width + 40


# Search Expenses
def search_expenses_window():
    expenses = load_file(EXPENSES_FILE)

    # Function to update the treeview based on the search key
    def update_treeview():
        for item in tree.get_children():
            tree.delete(item)
        key = search_entry.get()
        for expense in expenses:
            if key in expense[3].lower() or key == expense[2].lower():
                tree.insert("", "end", values=expense)
    window = create_window("Search Expenses", "600x400")

    tk.Label(window, text="Search Expenses", font=(FONT, 14, "bold")).pack(pady=10)
    tk.Label(window, text="Enter word to search").pack()
    search_entry = tk.Entry(window)
    search_entry.pack(pady=5)
    tk.Button(window, text="Search", command=update_treeview).pack(pady=20)
    tree = create_frame(window)
    update_treeview()


# Budget Alerts
def budget_alerts_window():
    total = sum_expenses()
    window = create_window("Budget Alerts", "550x300")
    tk.Label(window, text="Budget Alerts", font=(FONT, 16, "bold")).pack(pady=10)

    # Write the budget alerts
    for item in budget:
        category, limit = item[0], float(item[1])
        spent = total[category]
        if spent > limit:
            color = "red"
            text = f"{category}: OVER budget by {round(spent - limit, 2)}"
        else:
            color = "green"
            text = f"{category}: UNDER budget, remaining {round(limit - spent, 2)}"

        tk.Label(window, text=text, fg=color, font=(FONT, 12, "bold")).pack(padx=20, pady=5)


# Main Menu
def main_menu():
    # Main menu window
    menu = tk.Tk()
    menu.title("Personal Expense Manager")
    menu.geometry("400x400")
    # Title for the main menu
    tk.Label(menu, text="Personal Expense Manager", font=(FONT, 16, "bold")).pack(pady=20)
    # Buttons for the main menu
    tk.Button(menu, text="Add Expenses", width=20, command=add_expenses_window).pack(pady=10)
    tk.Button(menu, text="View Expenses", width=20, command=view_expenses_window).pack(pady=10)
    tk.Button(menu, text="Bar Chart", width=20, command=bar_chart_window).pack(pady=10)
    tk.Button(menu, text="Search Expenses", width=20, command=search_expenses_window).pack(pady=10)
    tk.Button(menu, text="Budget Alerts", width=20, command=budget_alerts_window).pack(pady=10)
    tk.Button(menu, text="Exit", width=20, command=menu.destroy).pack(pady=10)
    # Run the main menu
    menu.mainloop()


budget = load_file(BUDGET_FILE)
main_menu()
