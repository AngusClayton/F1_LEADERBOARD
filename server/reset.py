###THIS SCRIPT RESETS ALL TIMES FOR ALL TEAMS TO ZERO!!

import json
f = open("data.json","r")

a = json.loads(f.read())
f.close()

newlist = []

if input("Are you sure you want to reset all times (CTRL+C to cancel): ") == 'yes':
    print(".")

for i in a:
    a[i]['times'] = {0:999}
    a[i]['fast'] = 999

f = open("data.json","w")
f.write(json.dumps(a))
print("all times reset and written.")