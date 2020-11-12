"""
Zadanie: 5.1 Magazyn
"""

import sys
import csv
import os


operation_txt = ["Exit", "Show", "Add", "Sell", "Revenue", "Save", "Load"] #Revenue = Show_revenue
operation = 0

items = [
    {
    "name" : "Pyry",
    "quantity" : 50,
    "unit" : "kg",
    "unit_price": 1.52525
    },
    {
    "name" : "Cebula",
    "quantity" : 200,
    "unit" : "kg",
    "unit_price" : 1
    },
    {
    "name" : "Czosnek",
    "quantity" : 30,
    "unit" : "kg",
    "unit_price" : 2.525252525
    }
    ]

sold_items = []

if __name__ == "__main__":
    user_csv = ""
    if len(sys.argv) > 1:
        user_csv = sys.argv[1]


def curr_proj_path():
    """
    Function for getting current projekct file path. Just to save csv in the same directory.
    Only for Windows?
    Does not work with Bash - no permission/access to path :D
    """
    project_path = __file__
    head, tail = os.path.split(project_path)
    tail = tail #just to use it... inaczej podkreśla że nie wykorzystane :/
    return head


def operat(operation_txt):
    while True:
        in_operation = input("What would you like to do? ").capitalize()
        str_operation = in_operation.capitalize()

        if str_operation in operation_txt:
            if str_operation == "Exit":
                operation = 1
            elif str_operation == "Show":
                operation = 2
            elif str_operation == "Add":
                operation = 3
            elif str_operation == "Sell":
                operation = 4
            elif str_operation == "Revenue": #Revenue = Show_revenue
                operation = 5
            elif str_operation == "Save":
                operation = 6
            elif str_operation == "Load":
                operation = 7
        else:
            operation = 0
            print("I do not understand.")
            continue

        if operation != 0:
            break

    return operation


def get_items(items):
    print("Name\tQuantity\tUnit\tUnit Price (PLN)")
    print("%s\t%s\t%s\t%s" %(("_"*4), ("_"*8), ("_"*4), ("_"*10)))
    for i in range(len(items)):
        round_price = round(items[i]["unit_price"], 2)
        print("%s\t%s\t\t%s\t%s" %(items[i]["name"].capitalize(), items[i]["quantity"], items[i]["unit"], round_price))



def add_item():
    name = input("Item name: ").capitalize()
    quantity = int(input("Item quantity: "))
    unit = input("Item unit: ")
    unit_price = float(input("Item price per unit: "))
    item = {
        "name" : name,
        "quantity" : quantity,
        "unit" : unit,
        "unit_price" : unit_price
        }
    return item


def sell_item(items, sold_items=sold_items):
    name = input("Item name: ").capitalize()
    for i in range(len(items)):
        if items[i].get("name") == name:
            quantity = int(input("Quantity to sell: "))

            items[i]["quantity"] = items[i].get("quantity") - quantity
            print("Succesfully sold %d %s of %s" %(quantity, items[i].get("unit"), items[i].get("name")))
            get_items(items)

            sold = {
                "name" : items[i].get("name"),
                "quantity" : quantity,
                "unit" : items[i].get("unit"),
                "unit_price" : items[i].get("unit_price")
                }

            sold_items.append(sold)
            
    return items, sold_items

def get_costs(items):
    if len(items) != 0:
        costs_present = [items[i].get("quantity") * items[i].get("unit_price") for i in range(len(items))]
        costs_present = sum(costs_present)
    else:
        costs_present = 0
        print("Warehouse empty") #nigdy się nie wyświetli

    return costs_present


def get_income(sold_items):
    if len(sold_items) != 0:
        sold_cost = [sold_items[i].get("quantity") * sold_items[i].get("unit_price") for i in range(len(sold_items))]
        sold_cost = sum(sold_cost)
    else:
        sold_cost = 0
        print("Nothing has been sold")
        
    return sold_cost

def show_revenue(items=items, sold_items=sold_items):
    costs_present = get_costs(items)
    sold_cost = get_income(sold_items)
    revenue = costs_present - sold_cost

    print("Revenue breakdown (PLN)")
    print(f"Income: {sold_cost:.2f}")
    print(f"Costs: {costs_present:.2f}")
    print("-"*10)
    print(f"Revenue: {revenue:.2f}")


def export_items_to_csv(items):
    file_path = curr_proj_path() + "/" + "magazyn.csv"
    with open(file_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "quantity", "unit", "unit_price"])
        writer.writeheader()
        """
        tutaj miało być:
        writer.writerow(items) zamiast pętli ale daje błąd:

        wrong_fields = rowdict.keys() - self.fieldnames
        AttributeError: 'list' object has no attribute 'keys'
        """
        for item in items:
            writer.writerow(item)
    print("Successfully exported data to magazyn.csv")


def export_sales_to_csv(sold_items):
    file_path = curr_proj_path() + "/" + "magazyn_sold.csv"
    with open(file_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "quantity", "unit", "unit_price"])
        writer.writeheader()
        for item in sold_items:
            writer.writerow(item)
    print("Successfully exported data to magazyn_sold.csv")


def load_items_from_csv(items):
    file_path = curr_proj_path() + "/" + "magazyn.csv"
    items.clear()
    with open(file_path, "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for item in reader:
            item["quantity"] = int(item["quantity"])
            item["unit_price"] = float(item["unit_price"])
            items.append(item)
    print("Successfully loaded data from magazyn.csv")
    return items

def load_user_items_from_csv(items, user_csv=user_csv):
    file_path = user_csv
    items.clear()
    with open(file_path, "r", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for item in reader:
            item["quantity"] = int(item["quantity"])
            item["unit_price"] = float(item["unit_price"])
            items.append(item)
    print(f"Successfully loaded user data from {file_path}")
    return items



#tutaj wywołanie funkcji
#moglem jeszcze do menu dodac/zmodyfikowac save i load na:
# Save_D - with default path (mian.py path) / Save_U - with user defined path
# Load_D - with default path (mian.py path) / Load_U - with user defined path

if len(user_csv) > 1:
    load_user_items_from_csv(items)
else:
    pass

print(f"Welcome in Warehouse Manager! \nAvaliable options are: {operation_txt}")

while True:
    operation = operat(operation_txt)

    if operation == 1:
        print("Exiting... Bye!")
        exit()
    elif operation == 2:
        get_items(items)
    elif operation == 3:
        items.append(add_item())
        print("Succesfully added to warehouse. Current status:")
        get_items(items)
    elif operation == 4:
        items, sold_items = sell_item(items)
    elif operation == 5:
        show_revenue()
    elif operation == 6:
        export_items_to_csv(items)
        export_sales_to_csv(sold_items)
    elif operation == 7:
        items = load_items_from_csv(items)
    else:
        continue