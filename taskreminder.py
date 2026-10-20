import json
from datetime import datetime
import time

while True:
    cdt = datetime.now
    today = datetime(cdt.year, cdt.month, cdt.day)
    print(f"Checking logs at {datetime.now()}")
    with open('output/tasklogs.txt') as fp:
        lines = fp.read().splitlines()

    if len(lines) > 0:
        last = lines[-1]
    else:
        last = None

    if last is None:
        remind()
        continue

    date = datetime.strptime(last.split("|")[0], "%Y-%m-%d")
    log = json.loads(last.split("|")[1])

    if date < today:
        remind()

    else:
        print(log)


    time.sleep(1)
    # time.sleep(300)