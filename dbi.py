
import json, time
data = {}
with open('data.json') as json_file: #import data:
    data = json.load(json_file)


classes = []
#years = []
for i in data:
    tmp = data[i]['class']
    if tmp not in classes:
        classes.append(tmp)
    #if tmp.isnumeric() and tmp not in years:
    #    years.append(tmp)
print("Classes:",classes)
#print("Years:",years)

def getClasses():
    classes = []
    for i in data:
        tmp = data[i]['class']
        if tmp not in classes:
            classes.append(tmp)
    return classes



def getFastestTimes(teamNo):
    #get fastest react, fastest total, fastest
    totalF = {"time":9999,"run":0}
    reactF = {"time":9999,"run":0}
    carF = {"time":9999,"run":0}
    for i in data[teamNo]["times"]:
        cT = float(data[teamNo]["times"][i]["car"])
        rT = float(data[teamNo]["times"][i]["react"])
        tT = cT + rT
        if totalF["time"] > tT:
            totalF["time"] = tT
            totalF["run"] = i
        if reactF["time"] > rT:
            reactF["time"] = rT
            reactF["run"] = i
        if carF["time"] > cT:
            carF["time"] = cT
            carF["run"] = i
    return {"fastestTotal":totalF["time"],"fastestReaction":reactF["time"],"fast":carF["time"]}




##adds a new time entry for an existing team
def newEntry(teamNo,raceTime,reactTime):
    raceTime = float(raceTime)
    teamNo = str(teamNo)
    newRecord = {int(time.time()):{"car":raceTime,"react":reactTime}}
    data[teamNo]["times"].update(newRecord)
    #update fastest times:
    data[teamNo].update(getFastestTimes(teamNo))
    save()





##adds a new team to the json db
def newTeam(name,members,yrGroup,no,RACEtime,reactTime):
    no = str(no)
    yrGroup = yrGroup.upper()
    RACEtime = float(RACEtime)
    newRecord = {int(time.time()):{"car":RACEtime,"react":reactTime}}

    data.update({no:{"name":name,"class":yrGroup,"members":members,"times":newRecord,"fast":RACEtime,"fastestTotal":reactTime+RACEtime,"fastestReaction":reactTime}})
    save()
########## OOOPS I MADE A MISTAKE SUBS

##Change a previous time, refering to the time listed on  /team/22
def changeTeamRunTime(teamNo,runNo,time,react):
        saveAllow = True # Save Flag, turned off in dev versions
        runNo = int(runNo)
        time = float(time)
        no = str(teamNo)
        runs = data[no]["times"]
        print(runs)
        #now update runs to contain the correct data.
        hrRuns = {}
        counter = 1
        for i in runs:
                if counter == runNo:
                        prevTime = i[1]
                        print("timeModified: ",i)
                        if prevTime == data[no]["fast"]:
                                data[no]["fast"] = time
                        hrRuns.update({i:{"car":time,"react":react}})
                else:
                        hrRuns.update({i:runs[i]})
                counter += 1
        data[no]["times"] = hrRuns
        #fastest
        fastest = 999
        for i in data[teamNo]["times"]:
                if fastest > data[teamNo]["times"][i]:
                        fastest = data[teamNo]["times"][i]
        data[teamNo]["fast"] = fastest


        #save
        if saveAllow:
        #       data[no]["times"] = hrRuns
                save()
        else:
                print("NOSAVE")
                return hrRuns



##this sub changes the details of a team
### NOTE: DOES NOT WORK WITH TIMES, changeTeamRunTime sub handles this!!
def changeTeam(name,members,yrGroup,no):
    no = str(no)
    yrGroup = yrGroup.upper()
    prev = data[no]
    prev.update({"name":name,"class":yrGroup,"members":members})
    #prev.update({})
    data.update({no:prev})
    save()

##creates a new team, used for command-line access
def UiNewTeam():
    cont = input("Continue (Enter for yes, no for no)")
    while cont != "no":
        name = input("Team Name: ")
        inp = input("Member: ")
        members = inp.split(",")
        yrGroup = input("class: ")
        no = int(input("Team No:"))
        yrGroup = yrGroup.upper()
        RACEtime = float(input('time: '))
        newTeam(name,members,yrGroup,no,RACEtime)
        cont = input("Continue (Enter for yes, no for no)")
        save()
    print(data)

####DISPLAY Funcs

def sortList(sType): #sort by fastest
    teamFastest = {}
    for i in data:
        timeR = data[i]['fast']
        if sType == "react":
            timeR = data[i]['fastestReaction']
        elif sType == "total":
            timeR = data[i]['fastestTotal']

        teamFastest.update({i:timeR})
    speedSort = {k: v for k, v in sorted(teamFastest.items(), key=lambda item: item[1])}

    out = []
    for i in speedSort:
        tmp = data[i]
        tmp.update({"#":i})
        out.append(tmp)
    return out

#Year Filters
def Filter(x,sortT):
    x = str(x)
    out = []
    for i in sortList(sortT):
        if x in i['class']:
            out.append(i)
    return out



#class Filter:
def exactFilter(yr,sortT):
    out = []
    for i in sortList(sortT):
        if yr == i['class']:
            out.append(i)
    return out

#preconditions: valid data
#postconditions: All team times are removed.
def resetAllTimes():
    for i in data:
        data[i]['times'] = {str(int(time.time())): {'car': 999, 'react': 999}}
        data[i]['fastestTotal'] = 1998
        data[i]['fastestReaction'] = 999
        print(data[i]['times'])
    save()

def reset():
    global data
    data = {}
    save()


    
def backup():
    save()
    outputName = str(int(time.time())) + ".json"
    open(outputName, "w").write(open("data.json").read())
    line = outputName + ", " + str(time.ctime())
    open("files.txt", "a").write(line)

def restore(fileName):
    global data
    open("data.json", "w").write(open(fileName).read())
    with open('data.json') as json_file: #import data:
        data = json.load(json_file)

def listAllFiles():
    with open("files.txt", "r") as f:
        return f.readlines()

def save():
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    #backup()
    restore("1666924494.json")
    print(listAllFiles())
