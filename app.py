from flask import Flask,request,render_template
import dbi
app = Flask(__name__)
#Should hash this:
        return 2365

#index page
@app.route('/')
def index():
    classLinks = ""
    for i in dbi.getClasses():
        classLinks += "<a href='/year/{0}'>  {0} Leaderboard </a><br>".format(i)
    return render_template("index.html",class_Links=classLinks)

#API that returns a list of times based on filter conditions (<year>/class)
@app.route('/getTimes/<year>')
def getTimes(year):
    return dbi.Filter(year,request.args.get('sort'))

#show the leaderbaord for a year/class e.g. /year/6W for 6W or /year/6 for the entirety of year 6
@app.route('/year/<year>')
def year(year):
    return render_template('leaderboard.html',CLASS_ID=year)


#UI For adding a new time to board.
@app.route('/newEntry')
def newEntry():

    return render_template("newEntry.html")

#UI for adding new team to board
@app.route('/newTeam')
def newTeam():
    return render_template("newTeam.html")


#eww backend stuff for new data
@app.route('/submit',methods=["POST"])
def submitEntry():
    if int(request.form["pswd"]) == PSWD():
        dbi.newEntry(request.form["TeamNo"],request.form["Time"],request.form["react"])
        dbi.save()
        return 'Thankyou Click <a href="/newEntry"> Here </a> To go record another or: <a href="/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/newEntry"> Here </a> To go try again'

@app.route('/NewTeamSubmit',methods=["POST"])
def newTeamForm():
    if int(request.form["pswd"]) == PSWD():
        members = request.form["members"].split(",")
        outMembers = []
        for i in members:
            outMembers.append(i.strip())
        dbi.newTeam(request.form["name"],outMembers,request.form["yrGroup"],request.form["teamNo"],request.form["time"],request.form["react"])
        dbi.save()

        return 'Thankyou Click <a href="/NewTeamSubmit"> Here </a> To go record another or: <a href="/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/newEntry"> Here </a> To go try again'
####UPDATEING TEAMS
#updateing Times:
#times
#@app.route('/updateEntry')
#def updateEntry():
#    out = css
#    out += updateEntryHTML
#    return out
##updating team stat: (-Depreciated)
#@app.route('/updateTeam')
#def updateTeam():
    #out = css
    #out += updateTeamHTML
#    return render_template("updateTeam.html")


#ew backend stuff for updating times:
@app.route('/updateEntrySubmit',methods=["POST"])
def updateEntryForm():
    #changeTeamRunTime(teamNo,RunNo,time)
    if int(request.form["pswd"]) == PSWD():
        print(dbi.changeTeamRunTime(request.form["TeamNo"],request.form["Entry"],request.form["Time"],request.form["React"]))
        dbi.save()
        return 'Click<a href="/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/updateEntry"> Here </a> To go try again'
#ew backend stuff for updating team stat /details
@app.route('/updateTeamSubmit',methods=["POST"])
def updateTeamForm():
    if int(request.form["pswd"]) == PSWD():
        members = request.form["members"].split(",")
        outMembers = []
        for i in members:
            outMembers.append(i.strip())
        dbi.changeTeam(request.form["name"],outMembers,request.form["yrGroup"],request.form["teamNo"])
        dbi.save()
        return 'Thankyou Click <a href="/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/updateEntry"> Here </a> To go try again'


### DEEEP INFO ON TEAMS
@app.route('/team/<teamNo>')
def moreInfo(teamNo):
    record = dbi.data[teamNo]

    members = ", ".join(record['members'])

    ##TIMES
    timeList = []
    reactList = []
    totalList = []
    labelList = []
    counter = 1
    for i in record['times']:
        if int(record['times'][i]["car"]) < 10:
          timeList.append(record['times'][i]["car"])
          if record['times'][i]["react"] < 998:
            reactList.append(record['times'][i]["react"])
            totalList.append(record['times'][i]["react"] + record['times'][i]["car"])

          labelList.append(counter)
          counter += 1



    return render_template("moreInfo.html",NAME=record['name'],TEAMNO=teamNo,CLASS=record['class'],MEMBERS=members,FASTEST=str(record['fast']),TIMES_LIST=str(timeList),TOTAL_LIST=str(totalList),REACT_LIST=str(reactList),LABLES_LIST=str(labelList))


#===== edit all data modification 25/9/22

@app.route("/editData")
def displayAllDataEditor():
    data = dbi.data
    allDataPageHTML = ""
    for team in data:
        #generate the page:
        allDataPageHTML += "<tr><td>" + str(team) + "</td>"
        allDataPageHTML += "<td contenteditable>" + str(data[team]['name']) + "</td>"
        allDataPageHTML += "<td contenteditable>" + str(data[team]['class']) + "</td>"

        allDataPageHTML += "<td contenteditable>"
        allDataPageHTML += ", ".join(data[team]['members'])
        allDataPageHTML += "</td>"



        allDataPageHTML += "<td><table>"
        for time in data[team]['times']:

            #tmp1 = "<td>Car:</td><td contenteditable>" + str(data[team]['times'][time]['car']) + "</td><td>Reaction:</td><td contenteditable>" + str(data[team]['times'][time]['react']) + "</td>"
            #allDataPageHTML += "<span id=" + str(time) + ">"+ tmp1 + "</span>"
            allDataPageHTML += "<tr id=" + str(time) + "> <td>Car:</td><td contenteditable>" + str(data[team]['times'][time]['car']) + "</td><td>Reaction:</td><td contenteditable>" + str(data[team]['times'][time]['react']) + "</td>" + "</tr>"

        allDataPageHTML += "</table></td></tr>"


    return render_template('editData.html',row_data=allDataPageHTML)

@app.route("/saveData",methods=["POST"])
def saveDataFromEditor():
    newData = request.get_json()
    if 'pswd' in newData and newData['pswd'] == PSWD():
        del newData['pswd']




        print("Getting Data...")
        dbi.data = request.get_json()
        for team in dbi.data:
            dbi.data[team].update(dbi.getFastestTimes(team))
        print(dbi.data["333"])
        print("Saving Data...")
        dbi.save()
        return "OK"
    else:
        return "IPSWD"

@app.route("/getLatest/<year>")
def getLatest(year):
    tdata = []
    #get just time, team name etc
    for team in dbi.Filter(year,""):
      bt = 0
      lt = 0
      for i in team['times']:
        if int(i) > int(lt):
          lt = i
          bt = team['times'][i]
      tdata.append({"#":team["#"],"dt":lt,"time":bt,'name':team["name"]})
    tdata = sorted(tdata, key=lambda k: k['dt'], reverse=True)
    return tdata[0:3]

@app.route("/resetAllTimes",methods=["POST"])
def resetTimesAPI():
    if int(request.form["pswd"]) == PSWD():
        dbi.backup()
        dbi.resetAllTimes()
    return "<h1> All Times Have Been Reset</h1><a href='/'> Go home </a>"

@app.route("/reset",methods=["POST"])
def resetAllAPI():
    if int(request.form["pswd"]) == PSWD():
        dbi.backup()
        dbi.reset()
        return "<h1> All Data has been reset</h1><a href='/'> Go home </a>"


@app.route("/backup",methods=["POST"])
def backupAPI():
    if int(request.form["pswd"]) == PSWD():
        dbi.backup()
        return "<h1> Data has been backed up</h1><a href='/'> Go home </a>"
    return "Incorrect Password"


@app.route('/admin')
def admin():
    return render_template("manage.html")

if __name__ == '__main__':
    app.run(host='localhost',port='8000')
