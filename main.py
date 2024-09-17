from flask import Flask, request, render_template
import sqlite3
import dbi
# create db connection

def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

# create flask app
app = Flask(__name__)
##SET PASSWORD
## IF NO HTTPS; This should deffienetly be replaced by some rolling code like OAUTH 2FA
def PSWD():
	return 2365

def getTeam(teamNo):
    #if teamNo in dbi.data:
    #    return dbi.data[teamNo]
    #return None
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM teams WHERE id = ?", (teamNo,))
    team = cursor.fetchone() 
    return team

##Main list view
@app.route('/leaderboard/<filter>')
def leaderboard(filter):
    return render_template('board.html')

## Index page
@app.route('/')
def index():
    return render_template('index.html')


##### ADDING NEW DATA
#times
@app.route('/newEntry')
def newEntry():
    out = css
    out += newEntryHTML
    return out

#teams
@app.route('/newTeam')
def newTeam():
    out = css
    out += newTeamHTML
    return out
#eww backend stuff for new data
@app.route('/submit',methods=["POST"])
def submitEntry():
    if int(request.form["pswd"]) == PSWD():
        dbi.newEntry(request.form["TeamNo"],request.form["Time"])
        dbi.save()
        return 'Thankyou Click <a href="/leaderboard/newEntry"> Here </a> To go record another or: <a href="/leaderboard/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/leaderboard/newEntry"> Here </a> To go try again'

@app.route('/NewTeamSubmit',methods=["POST"])
def newTeamForm():
    if int(request.form["pswd"]) == PSWD():
        members = request.form["members"].split(",")
        outMembers = []
        for i in members:
            outMembers.append(i.strip())
        dbi.newTeam(request.form["name"],outMembers,request.form["yrGroup"],request.form["teamNo"],request.form["time"])
        dbi.save()
        return 'Thankyou Click <a href="/leaderboard/NewTeamSubmit"> Here </a> To go record another or: <a href="/leaderboard"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/leaderboard/newEntry"> Here </a> To go try again'
####UPDATEING TEAMS
#updateing Times:
#times
@app.route('/updateEntry')
def updateEntry():
    out = css
    out += updateEntryHTML
    return out
##updating team stat:
@app.route('/updateTeam')
def updateTeam():
    out = css
    out += updateTeamHTML
    return out


#ew backend stuff for updating times:
@app.route('/updateEntrySubmit',methods=["POST"])
def updateEntryForm():
    #changeTeamRunTime(teamNo,RunNo,time)
    if int(request.form["pswd"]) == PSWD():
        print(dbi.changeTeamRunTime(request.form["TeamNo"],request.form["Entry"],request.form["Time"]))
        dbi.save()
        return 'Click<a href="/leaderboard/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/leaderboard/updateEntry"> Here </a> To go try again'
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
        return 'Thankyou Click <a href="/leaderboard"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="/leaderboard/updateEntry"> Here </a> To go try again'


### DEEEP INFO ON TEAMS
@app.route('/team/<teamNo>')
def moreInfo(teamNo):
    record = getTeam(teamNo)
    if record == None:
        return render_template('error.html', message="Team not found")
    members = ", ".join(record['members'])
    ##TIMES
    timeList = []
    labelList = []
    counter = 1
    for i in record['times']:
        timeList.append(record['times'][i])
        labelList.append(counter)
        counter += 1
   



    return render_template('moreInfo.html', name=record['name'], members=members, tclass=record['class'], fastest = str(record['fast']), chartLabels=str(labelList), chartTimes=str(timeList))


if __name__ == '__main__':
    app.run(host='localhost',port='8000')
