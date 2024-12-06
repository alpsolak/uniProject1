import turtle
from datetime import datetime

# File paths for expenses and budget
EXPENSES_FILE = "expenses.txt"
BUDGET_FILE = "budget.txt"


# Function to load data from a file
def load_file(file):
    try:
        with open(file, "r") as f:
            return [i.strip().split("\t") for i in f.readlines()]
    except FileNotFoundError:
        return []


# Function to save a new expense to the expenses file
def save_expense(expense):
    with open(EXPENSES_FILE, "a") as f:
        f.write("\t".join(expense) + "\n")


# Function to validate the date format
def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Function to add a new expense
def add_expenses():
    while True:
        date = input("Date (YYYY-MM-DD): ")
        if validate_date(date):
            break
        else:
            print("Please enter a valid date in YYYY-MM-DD format.")
    while True:
        try:
            amount = float(input("Amount: "))
            break
        except ValueError:
            print("Please enter a valid number")
    while True:
        category = input("Category(Food, Housing, Transportation, Education, Entertainment, Shopping, Other): ")
        if category in ["Food", "Housing", "Transportation", "Education", "Entertainment", "Shopping", "Other"]:
            break
        else:
            print("Please enter a valid category")
    description = input("Description: ")
    expense = [date, str(amount), category, description]
    save_expense(expense)
    print("Expense added successfully!")


# Function to view expenses
def view_expenses(expenses):
    choice = input("All or specific category (all/c): ").lower()
    if choice == "all":
        for expense in expenses:
            print("\t".join(expense))
    else:
        categories = {}
        for expense in expenses:
            category = expense[2]
            if category not in categories:
                categories[category] = []
            categories[category].append(expense)
        for category, items in categories.items():
            print(f"\n{category}:")
            for item in items:
                print("\t".join(item))


# Function to calculate total expenses per category
def total_expenses(expenses):
    categories = {"Food": 0, "Housing": 0, "Transportation": 0, "Education": 0,
                  "Entertainment": 0, "Shopping": 0, "Other": 0}
    for expense in expenses:
        category = expense[2]
        categories[category] += float(expense[1])
    return categories


# Function to draw a bar chart of expenses
def bar_chart(total):
    wn = turtle.Screen()
    wn.bgcolor("lightgreen")
    wn.setup(width=700, height=500)  # Adjust the window size as needed
    wn.tracer(0)
    alex = turtle.Turtle()
    alex.pensize(5)
    alex.speed(0)
    legend = turtle.Turtle()
    legend.hideturtle()
    namer = turtle.Turtle()
    namer.hideturtle()
    alex.hideturtle()
    alex.penup()
    alex.goto(-320, -220)
    alex.pendown()
    alex.left(90)
    colors = ["red", "blue", "green", "orange", "purple", "yellow", "darkcyan"]
    for i, (category, amount) in enumerate(total.items()):
        alex.color(colors[i % len(colors)])
        alex.begin_fill()
        alex.forward(amount)
        alex.right(90)
        alex.forward(50)
        alex.right(90)
        alex.forward(amount)
        alex.left(90)
        alex.penup()
        alex.forward(25)
        alex.pendown()
        alex.end_fill()
        alex.left(90)
        namer.penup()
        namer.goto(alex.xcor() - 50, -250 + amount + 40)
        namer.write(f"{amount}", align="center", font=("Arial", 10, "normal"))
    legend.penup()
    legend.goto(225, 200)
    for i, category in enumerate(total.keys()):
        legend.color(colors[i % len(colors)])
        legend.dot(10)
        legend.penup()
        legend.forward(20)
        legend.write(category, align="left", font=("Arial", 10, "normal"))
        legend.backward(20)
        legend.right(90)
        legend.forward(20)
        legend.left(90)
    wn.update()
    wn.exitonclick()


# Function to search expenses by a keyword
def search_expenses(expenses):
    word = input("Enter a word to search for: ").lower()
    for expense in expenses:
        if word in expense[3].lower() or word in expense[2].lower():
            print("\t".join(expense))


# Function to check budget alerts
def budget_alerts(total, budget):
    for item in budget:
        category, limit = item[0], float(item[1])
        if total[category] > limit:
            print(f"Limit exceeded in {category}.")
        else:
            remaining = round(limit - total[category], 2)
            print(f"Remaining budget for {category}: {remaining}")


# Main menu function
def menu():
    functions = [[add_expenses, []],
                 [view_expenses, []],
                 [bar_chart, []],
                 [search_expenses, []],
                 [budget_alerts, []],
                 [exit, []]]
    text = ("1. Add Expenses\n"
            "2. View Expenses\n"
            "3. Produce Bar Chart for Expenses\n"
            "4. Search Expenses\n"
            "5. Budget Alerts\n"
            "6. Exit\n")
    while True:
        expenses = load_file(EXPENSES_FILE)
        budget = load_file(BUDGET_FILE)
        total = total_expenses(expenses)
        functions[1][1] = [expenses]
        functions[2][1] = [total]
        functions[3][1] = [expenses]
        functions[4][1] = [total, budget]
        try:
            option = int(input(text))
            if 0 < option < 7:
                func, args = functions[option - 1]
                func(*args)
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Please enter a valid number.")


# Run the menu
menu()
