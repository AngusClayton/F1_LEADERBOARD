
import json, time
#HTML
topTable = """
<style>
a {
  color: white; /* blue colors for links too */
  text-decoration: underline; /* no underline */
}
</style>
<table style='width:100%'>
<colgroup>
<col " width="10%">
<col width="10%">
<col  width="40%">
<col  width="20%">
<col  width="10%">
</colgroup>


<tr><th>#</th><th>Team No</th><th>Team Name</th><th>Time</th><th>Class</th></tr>"""




#{TeamNo:{"name":"teamAwesome","class":"6L","members":["name","name"],"times":{date:timeRace}}}
#data = {1:{"name":"teamAwesome","class":"4L","members":["name","name"],"times":{156666:999},"fast":999},2:{"name":"VeryCool","class":"4L","members":["name","2"],"times":{156666:979},"fast":979}}
data = {}
with open('data.json') as json_file: #import data:
    data = json.load(json_file)

##adds a new time entry for an existing team
def newEntry(teamNo,raceTime):
    raceTime = float(raceTime)
    teamNo = str(teamNo)
    newRecord = {int(time.time()):raceTime}
    data[teamNo]["times"].update(newRecord)
    #see fastest
    fastest = data[teamNo]["fast"]
    for i in data[teamNo]["times"]:
        if fastest > data[teamNo]["times"][i]:
            fastest = data[teamNo]["times"][i]
    data[teamNo]["fast"] = fastest

##adds a new team to the json db
def newTeam(name,members,yrGroup,no,RACEtime):
    no = str(no)
    yrGroup = yrGroup.upper()
    RACEtime = float(RACEtime)
    newRecord = {int(time.time()):RACEtime}
    data.update({no:{"name":name,"class":yrGroup,"members":members,"times":newRecord,"fast":RACEtime}})
    save()
########## OOOPS I MADE A MISTAKE SUBS

##Change a previous time, refering to the time listed on  /team/22
def changeTeamRunTime(teamNo,runNo,time):
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
			hrRuns.update({i:time})
		else:
			hrRuns.update({i:runs[i]})
		counter += 1
	#save
	if saveAllow:
		data[no]["times"] = hrRuns
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

def sortList(): #sort by fastest
    teamFastest = {}
    for i in data:
        teamFastest.update({i:data[i]['fast']})
    speedSort = {k: v for k, v in sorted(teamFastest.items(), key=lambda item: item[1])}
    
    out = []
    for i in speedSort:
        tmp = data[i]
        tmp.update({"#":i})
        out.append(tmp)
    return out

#Year Filters
def FilterYear4():
    out = []
    for i in sortList():
        if '4' in i['class']:
            out.append(i)
    return out

def FilterYear6():
    out = []
    for i in sortList():
        if '6' in i['class']:
            out.append(i)
    return out

#class Filter:
def classFilter(yr):
    out = []
    for i in sortList():
        if yr == i['class']:
            out.append(i)
    return out

### HTML TABLE RENDERER: (clist, title)
def render(clist,yr):
    output = "<h1>" + yr + " Leaderboard</h1>" + topTable
    counter = 1 #position
    for i in clist:
        if counter == 1:
            output += "<tr class='first'>"
        elif counter == 2:
            output +=  "<tr class='second'>"
        elif counter == 3:
            output +=  "<tr class='third'>"
        else:
            output += "<tr>"
        #<tr><th>#</th><th>Team No</th><th>Team Name</th><th>Time</th><th>Class</th></tr>
        #[{'name': 'VeryCool', 'class': '4L', 'members': ['name', '2'], 'times': {156666: 979}, 'fast': 979, '#': 2}
        output += "<td>" + str(counter) + "</td>"
        output += "<td>" + str(i['#']) + "</td>"
        output += "<td> <a href='/leaderboard/team/" + str(i['#']) + "'>"+ str(i['name']) + "</a></td>"
        output += "<td>" + str(i['fast']) + "</td>"
        output += "<td>" + str(i['class']) + "</td>"

        output +="</tr>"
        counter +=1 #position
    output +="</table>"
    return output

def save():
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
