import turtle

EXPENSES_FILE = "expenses.txt"
BUDGET_FILE = "budget.txt"


def load_files():
    try:
        with open(EXPENSES_FILE, "r") as file:
            expenses_file = [i.strip().split("\t") for i in file.readlines()]
    except FileNotFoundError:
        expenses_file = []
    try:
        with open(BUDGET_FILE, "r") as file:
            budget_file = [i.strip().split("\t") for i in file.readlines()]
    except FileNotFoundError:
        budget_file = []
    return expenses_file, budget_file


def add_expenses():
    date = input("Date (YYYY-MM-DD): ")
    amount = input("Amount: ")
    category = input("Category: ")
    description = input("Description: ")
    a = [date, amount, category, description]
    with open(EXPENSES_FILE, "a") as file:
        file.write("\t".join(a) + "\n")


def view_expenses(expenses):
    cst = input("All or specific category(all/c): ").lower()
    if cst == "all":
        for i in expenses:
            print("\t".join(i))
    else:
        categories = {}
        for i in expenses:
            category = i[2]
            if category not in categories:
                categories[category] = []
            categories[category].append(i)
        for i, j in categories.items():
            print(f"\n{i}:")
            for k in j:
                print("\t".join(k))


def total_expenses(expenses):
    categories = {"Food": 0, "Housing": 0, "Transportation": 0, "Education": 0, "Entertainment": 0, "Shopping": 0, "Other": 0}
    for i in expenses:
        category = i[2]
        categories[category] += float(i[1])
    return categories


def bar_chart(total):
    wn = turtle.Screen()
    wn.bgcolor("lightgreen")
    # Alex draws the bars
    alex = turtle.Turtle()
    alex.pensize(5)
    alex.speed(10)

    # Namer writes names
    namer = turtle.Turtle()
    namer.hideturtle()
    alex.hideturtle()
    namer.penup()

    alex.penup()
    alex.forward(-150)
    alex.pendown()

    namer.forward(-100)
    alex.left(90)
    for i in total:
        alex.forward(total[i])
        alex.right(90)
        alex.forward(100)
        alex.right(90)
        alex.forward(total[i])
        alex.left(180)
        namer.write(str(i), align="center", font=("Arial", 10, "normal"))
        namer.forward(100)
    wn.exitonclick()


def search_expenses(expenses):
    word = input("Enter a word to search for: ").lower()
    for i in expenses:
        if word in i[3].lower() or word in i[2].lower():
            print("\t".join(i))


def budget_alerts(total, budget):
    for i in budget:
        if total[i[0]] > float(i[1]):
            print(f"{i[0]} kategorisinde limiti aştınız.")
        else:
            print(f"{i[0]} için kalan limitiniz: {round((float(i[1])-total[i[0]]), 2)}")


def menu():
    expenses, budget = load_files()
    total = total_expenses(expenses)
    functions = [(add_expenses, []),
                 (view_expenses, [expenses]),
                 (bar_chart, [total]),
                 (search_expenses, [expenses]),
                 (budget_alerts, [total, budget]),
                 (exit, [])]
    text = ("1. Add Expenses\n"
            "2. View Expenses\n"
            "3. Produce Bar Chart for Expenses\n"
            "4. Search Expenses\n"
            "5. Budget Alerts\n"
            "6. Exit\n")
    while True:
        try:
            option = int(input(text))
            if 0 < option < 8:
                func, args = functions[option - 1]
                func(*args)
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Please enter a number.")


menu()
