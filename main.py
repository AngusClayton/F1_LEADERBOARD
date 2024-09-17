from flask import Flask, request, render_template, Response
import sqlite3
import dbi
import traceback


# create db connection
def get_db_connection():
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor


##SET PASSWORD
## IF NO HTTPS; This should deffienetly be replaced by some rolling code like OAUTH 2FA
def PSWD():
	return '2365'
# ==================== DATABASE METHODS =================
#preconditions: teamNo
#postconditions: returns team data
def getTeam(teamNo):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM teams WHERE id = ?", (teamNo,))
    team = cursor.fetchone() 
    conn.close()
    return team

#preconditions: teamNo
#postconditions: returns all times for a team; sorted chronologically
def getTeamTimes(teamNo):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM times WHERE team_id = ? ORDER BY id", (teamNo,))
    
    times = cursor.fetchall()
    conn.close()
    return times

#preconditions: teamNo
#postconditions: returns the fastest time for a team
def getFastestTime(teamNo):
    conn, cursor = get_db_connection()
    cursor.execute('''
        SELECT MIN(time_record) AS fastest_time
        FROM times
        WHERE team_id = ?
    ''', (teamNo,))
    result = cursor.fetchone()
    conn.close()
    if result == None:
        return 999
    return result['fastest_time']
#preconditions: filter e.g. 4W or 5W, or 5 for all 5th years
#postconditions: returns a list of teams with their fastest times
def getLeaderboard(filter):
    # wild card, return whole DB
    if filter == '*':
        filter = ''
    filter = f"%{filter}%"
    conn, cursor = get_db_connection()
    cursor.execute('''
    SELECT te.id, te.name, te.class, MIN(t.time_record) AS fastest_time
    FROM teams te
    LEFT JOIN times t ON te.id = t.team_id
    WHERE te.class LIKE ?
    GROUP BY te.id, te.name
    ORDER BY 
    CASE WHEN MIN(t.time_record) IS NULL THEN 999 ELSE MIN(t.time_record) END;
    ''', (filter,))
    teams = cursor.fetchall()
    # get teams with no time
    conn.close()
    return teams

#preconditions: none
#postconditions: returns all distinct classes in table
def getClasses():
    conn, cursor = get_db_connection()
    cursor.execute('''
    SELECT DISTINCT class
    FROM teams
    ORDER BY class;
    ''')
    classes = cursor.fetchall()
    conn.close()

    if classes == None:
        return []

    return set(item['class'] for item in classes)

#preconditions: teamNo
#postconditions: checks if team exists:
def teamExists(teamNo):
    conn, cursor = get_db_connection()
    cursor.execute('''
    SELECT COUNT(*)
    FROM teams
    WHERE id = ?
    ''', (teamNo,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

# ============== PAGE METHODS ============
# create flask app
app = Flask(__name__)

## Main List View
@app.route('/leaderboard/<filter>')
def leaderboard(filter):
    teams = getLeaderboard(filter)
    filterDesc = None
    if filter.isnumeric():
        filterDesc = "Year " + filter
    elif filter=="*":
        filterDesc = "All Students "
    else:
        filterDesc = "Class " + filter
    return render_template('board.html', teams=teams, desc=filterDesc)

## Index page
@app.route('/')
def index():
    # determine what links to present
    classes = getClasses()
    groups = []
    for i in classes:
        if i[0] not in groups:
            groups.append(i[0])
    
    return render_template('index.html', classes=classes, groups=groups)

### Team Info Page
@app.route('/team/<teamNo>')
def moreInfo(teamNo):
    # get team from db
    record = getTeam(teamNo)
    # if team invalid; error and redirect
    if record == None:
        return render_template('error.html', message="Team not found")
    members = record['members']

    # calculate graph
    timeList = []
    labelList = []
    count = 1
    for i in getTeamTimes(teamNo):
        timeList.append(i['time_record'])
        labelList.append(count)
        count+=1
    # render and return
    return render_template('moreInfo.html', number=str(teamNo), name=record['name'].title(), members=members, tclass=record['class'], fastest = getFastestTime(teamNo), chartLabels=str(labelList), chartTimes=str(timeList))

### Add Team Page
@app.route('/addTeam')
def admin():
    return render_template('addTeam.html')

## Add Time Page
@app.route('/addTime')
def addTime():
    return render_template('addTime.html') 

# edit team page
# lists all teams; then you can hit edit
@app.route('/editTeam', methods=['GET'])
def editTeam():
    # get all teams
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall() 
    #print(teams)
    conn.close()
    return render_template('editTeam.html', teams = teams) 

# edit team page
# has details of a specific team
@app.route('/editTeam/<teamNo>')
def editTeamPage(teamNo):
    # get team from db
    team = getTeam(teamNo)
    times = getTeamTimes(teamNo)
    #print(dict(team))
    #for t in times:
    #    print(dict(t))
    # if team invalid; error and redirect
    if team == None:
        return render_template('error.html', message="Team not found")
   
    return render_template('editATeam.html', team=team, times=times)


##======== API METHODS
# add a new team
@app.route('/submitTeam', methods=['POST'])
def submitTeam():
    # get form data
    data = request.get_json()
    print(data)
    # check if team already exists:
    if teamExists(data['number']):
        return Response(status=409) # conflict status

    # check password
    if data['pswd'] != PSWD():
        return Response(status=401)
    
    # clean up data
    members = data['members']
    members = [i.strip().title() for i in members]
    members = ', '.join(members)
    


    # attempt to add team

   #
    try:
        conn, cursor = get_db_connection()
        # insert team
        cursor.execute('INSERT INTO teams (id, name, members, class) VALUES (?, ?, ?, ?)', 
                    (data['number'], data['name'].title().strip(), members, data['className'].strip().upper()))
        
        conn.commit() # save to db

    except Exception as e:
        print("Exception whilst inserting team into DB")
        print(e)
        return Response(status=500)
    
    return Response(status=200)

# add a time
@app.route('/addTime', methods=['POST'])
def addTimeAPI():
    # get form data
    data = request.get_json()
    print(data)
    # check if team  exists:
    if teamExists(data['team']) == False:
        return Response(status=404) # conflict status

    # check password
    if data['pswd'] != PSWD():
        return Response(status=401)
    
    # attempt add
    try:
        conn, cursor = get_db_connection()
        # insert team
        cursor.execute('INSERT INTO times (team_id, time_record) VALUES (?, ?)', 
                    (data['team'], data['time']))
        
        conn.commit() # save to db

    except Exception as e:
        print("Exception whilst inserting time into DB")
        print(e)
        return Response(status=500)
    
    return Response(status=200)

# edit a team
@app.route('/editTeam', methods=['POST'])
def editTeamSubmit():   
    data = request.get_json()

    # check if team  exists:
    if teamExists(data['teamID']) == False:
        return Response(status=404) # conflict status

    # check password
    if data['pswd'] != PSWD():
        return Response(status=401)
    
    # clean data
    members = data['teamMembers'].split(", ")
    members = [i.strip().title() for i in members]
    members = ', '.join(members)
    

    # try update team table:
    try:
        conn, cursor = get_db_connection()
        # insert team
        cursor.execute('UPDATE teams SET name = ?, members = ?, class = ? WHERE id = ?', 
                    (data['teamName'].title().strip(), members, data['teamClass'].strip().upper(), data['teamID']))
        
        conn.commit()
    except Exception as e:
        print("Exception whilst updating team in DB")
        print(e)
        return Response(status=500)
    
    # try update times table
    try:
        # delete all times
        cursor.execute('DELETE FROM times WHERE team_id = ?', (data['teamID'],))
        conn.commit()
        # add back in times
        for i in data['timeRecords']:
            if float(i) > 0:
                cursor.execute('INSERT INTO times (team_id, time_record) VALUES (?, ?)', 
                        (data['teamID'], i))
                conn.commit()
    except Exception as e:
        print("Exception whilst updating times in DB")
        print(e)
        traceback.print_exc()
        return Response(status=500)

    return Response(status=200)

if __name__ == '__main__':
    app.run(host='localhost',port='8000',debug=True)
