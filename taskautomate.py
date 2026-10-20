import pyinputplus as pyip
import json
from icecream import ic

with open('tasklist.json') as fp:
    db = json.load(fp)
    tasks = db['tasks']
    workers = db['humans']

while True:
    mainmenu = [
        "Assign task",
        "Check tasks",
        "Mark completed",
        "Add Task",
        "Update Task",
        "Add Human",
        "Update Human",
        "Exit",
    ]
    match pyip.inputMenu(mainmenu, "Choose an option:\n", numbered=True):
        case "Assign task":
            worker = workers[pyip.inputMenu(list(workers.keys()), "Choose a worker:\n", numbered=True)]
            possible = [t for t, v in tasks.items() if v['timeframe'] < worker["time"]]
            task = pyip.inputMenu(possible, "Select a task from the list:\n", numbered=True)
            worker['assigned'].append(task)
            worker['time'] -= tasks[task]['timeframe']

        case "Check tasks":
            tasklist = list(tasks.keys())
            for worker in workers:
                w = workers[worker]
                if len(w['assigned']) == 0:
                    print(f'Worker {worker} has no task assigned!')

                else:
                    print(f'Worker {worker} has the following task assigned:')
                    for t in w['assigned']:
                        print(f'  - {t}')
                    tasklist = [t for t in tasklist if t not in w['assigned']]
            if len(tasklist) != 0:
                print('Unassigned Tasks:')
                for t in tasklist:
                    print(f'  - {t}')

        case "Mark completed":
            completable =[]
            for worker in workers:
                w = workers[worker]
                if len(w['assigned']) == 0:
                    print(f'Worker {worker} has no task assigned!')
                else:
                    print(f'Worker {worker} has the following task assigned:')
                    for t in w['assigned']:
                        completable.append(t)
                        print(f'  - {t}')
            completed = pyip.inputMenu(completable + ["None"], "Which task has been completed?\n", numbered=True)
            if completed == "None":
                continue
            else:
                for w in workers:
                    worker = workers[w]
                    if completed in worker['assigned']:
                        break
                else:
                    print("Could not find worker")
                    continue
                
                workers[w]['assigned'] = [t for t in worker['assigned'] if t != completed]
                workers[w]['time'] += tasks[completed]['timeframe']
                    
        case "Add Task":
            name = pyip.inputStr("Enter task name: ")
            task = {
                "age": {
                    "min": pyip.inputInt("Enter minimum age requirement: "),
                    "max": pyip.inputInt("Enter maximum age limit: ")
                },
                "reminder": 0,
                "timeframe": pyip.inputFloat("Enter the timeframe in hours: "),
                "status": None
            }
            tasks[name] = task

        case "Update Task":
            name = pyip.inputMenu(list(tasks.keys()), "Select a task from the list:\n", numbered=True)
            attribute = pyip.inputMenu(list(tasks[name].keys()), "Select a task from the list:\n", numbered=True)
            tasks[name][attribute] = pyip.inputFloat(f"Enter the new value for {attribute}: ")

        case "Add Human":
            name = pyip.inputStr("Enter human name: ")
            human = {
                "age": pyip.inputInt("Enter their age: "),
                "time": pyip.inputFloat("Enter their available time in hours: "),
                "assigned": []
            }
            workers[name] = human

        case "Update Human":
            name = pyip.inputMenu(list(workers.keys()), "Choose a worker:\n", numbered=True)
            attribute = pyip.inputMenu(list(workers[name].keys()), "Select a task from the list:\n", numbered=True)
            workers[name][attribute] = pyip.inputFloat(f"Enter the new value for {attribute}: ")

        case _:
            with open('tasklist.json', 'w') as fp:
                json.dump({"humans": workers, "tasks": tasks}, fp, indent=2)

            break
