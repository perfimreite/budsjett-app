import json
import numpy as np
import matplotlib.pyplot as plt


# goes through the different expense areas and takes the get user input for each
def get_user_expenses():
    expenses = []

    for i in range(len(expense_areas) - 1):
        question = f"Kor mykje har du brukt på {expense_areas[i]} denne månaden: "
        expenses.append(int(input(question)))

    store_data(expenses)

    return expenses


# takes data from user input and stores it in the "history.json" file
def store_data(expenses):
    path = "./history.json"
    
    with open (path, "r", encoding="utf-8") as file:
        data = json.load(file)

        end = len(expenses)
        sum = 0
        previous_expenses = data["history"]["expenses"].values()

        for i, value in zip(range(0, end), previous_expenses):
            sum += expenses[i]
            value.append(expenses[i])
            
        data["history"]["expenses"]["total"].append(sum)

    with open (path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# find the differences between his bugdet and actual purchases for the month 
def compare_with_budget(expenses, expected_expenses):
    delta = 0
    total = 0
    deltas = []

    l = len(expected_expenses) - 1

    for i in range(l):
        d = expected_expenses[i] - expenses[i]
        delta += d
        deltas.append(d)
        total += expenses[i]


    l = len(deltas) - 1
    biggest_delta = 0
    biggest_spend = ""

    for i in range(l):
        if abs(deltas[i]) > biggest_delta:
            biggest_delta = abs(deltas[i])
            biggest_spend = expense_areas[i]

    return [delta, biggest_spend, total]


# look at how much he spent compared to his budget and give feedback accordingly
def review_result(result):
    delta = result[0]
    biggest_spend = result[1]
    total = result[2]
    expenses.append(total)

    if delta == 0:
        review = "Du brukte akkurat så mykje pengar som du hadde planlagt."
    elif delta < 0:
        review = f"Denne månaden brukte du {abs(delta)} kroner for mykje...\nDu burde bruka mindre pengar på {biggest_spend} enn det du har gjort i det siste."
    else:
        review = f"Godt jobbba, du sparte {delta} kroner denne månaden, Det kan vera ein god ide å setja desse pengane på sparekontoen din, eller berre invister alt i Bitcoin..."

    return review


# gets the average from all the users stored data
def get_user_average():
    path = "./history.json"
    average = []

    with open (path, "r", encoding="utf-8") as file:
        data = json.load(file)
        history = data["history"]["expenses"].values()

        for h in history:
            sum = 0
            for num in h:
                sum += num

            a = sum / len(h) 
            average.append(a)
            
    return average


# make the graphs and give the user feedback on his latest month
def give_feedback(eval):
    # feedback
    print(f"RESULT: {eval}")
   
    # graph
    average = get_user_average()
    x = np.arange(len(expense_areas))
    WIDTH = 0.30

    plt.bar(x - WIDTH, expected_expenses, width=WIDTH, label='Budsjett', color='gray')
    plt.bar(x, expenses, width=WIDTH, label='Utgifter', color='blue')
    plt.bar(x + WIDTH, average, width=WIDTH, label='Gjennomsnitt', color='orange')
    plt.xlabel('Utgiftsområder')
    plt.ylabel('Kroner')
    plt.title('Ditt budsjett, månadens utgifter, og dine gjennomsnittsutgifter')
    plt.xticks(x, expense_areas)
    plt.show()
    

# read data from the budget and sort it into lists
def handle_data():
    path = "./budget.json"

    with open(path, "r", encoding="utf-8") as file:
        budget = json.load(file)
        currency = budget["budget"]["unit"]
        expense_areas = []
        expected_expenses = []

    for k, v in budget["budget"]["expenses"].items():
        expense_areas.append(k)    
        expected_expenses.append(v)    
        
    return [expense_areas, expected_expenses]


# execute  program
expense_areas, expected_expenses = handle_data()
expenses = get_user_expenses()
result = compare_with_budget(expenses, expected_expenses)
eval = review_result(result)
feedback = give_feedback(eval)

print(feedback)
