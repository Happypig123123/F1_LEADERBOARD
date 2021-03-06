from flask import Flask,request
from flask import send_file
import dbi
app = Flask(__name__)



##SET PASSWORD
## IF NO HTTPS; This should deffienetly be replaced by some rolling code like OAUTH 2FA
def PSWD():
	return 2365

### PRE URL:::
preURL = '' #for reverse proxy use


### MORE INFO TEMPLATE
moreInfoHTML = """<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
<style>
.cc {
    height:40vh;
}
.sub {
    color:yellow;
}
</style>

<h1> ###NAME <span class="sub">####TEAMNO</span></h1>
Class: <span class = "SUB"> ###CLASS </span>
<h2>Members:</h2><span class="sub">
###MEMBERS</span>
<h2>Best Time: <u class='sub'>###FASTESTs</u></h2>
<h2>Race History </h2>
In Milliseconds, Lower is better. Hover over points to see times. <br>
<div class="cc">
<canvas id="myChart"></canvas></div>
<script>
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ###LABLES_LIST,
        datasets: [{
            label: 'Times',
            borderColor: 'rgb(255, 255, 0)',
            data: ###TIMES_LIST
        }]
    },

    // Configuration options go here
    options: {
         responsive: true,
        maintainAspectRatio: false,

    }
});

</script>
"""





###MORE HTML (CSS)
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300&family=Exo:wght@300;800&display=swap');
body{
    background-color: #111111;
    color: white;
    font-family: 'Exo', sans-serif;
    font-size:150%;
}
table {
  border-collapse: collapse;
  width:100%;
  font-size:150%;
  border-color: #6b6566;
}

th, td {
  border-bottom: 1px solid #ddd;
  padding:15px;
  text-align: left;
}

.first{
    color:#fcdb05;
    background-color:#35311a;
}
.second{
    color:#91c6c1;
    background-color:#152322;
}
.third{
    color:#cd7f32;
    background-color:#261b10;
}
</style>
"""
newEntryHTML = """<!DOCTYPE html>
<html>
<body>

<h2>New Race Result Record:</h2>

<form action="$$$LEADERBOARD/submit" method="POST">
    <h1> Team Details</h1>

 <label for="lname">Team Number: (Must be exact!)</label><br>
  <input type="text" id="TeamNo" name="TeamNo" value="00"><br><br>

  <label for="lname">Time:</label><br>
  <input type="text" id="TeamNo" name="Time" value="1.111"><br><br>

  <label for="lname">Password:</label><br>
  <input type="password" id="s" name="pswd" value="0"><br><br>

  <input type="submit" value="Submit">
</form>

<p>Click Submit to continue</p>

</body>
</html>

"""
newEntryHTML = newEntryHTML.replace("$$$LEADERBOARD",preURL)
updateEntryHTML = """<!DOCTYPE html>
<html>
<body>

<h2>Update Race Result Record:</h2>

<form action="$$$LEADERBOARD/updateEntrySubmit" method="POST">
    <h1> Team Details</h1>

 <label for="lname">Team Number: (Must be exact!)</label><br>
  <input type="text" id="TeamNo" name="TeamNo" value="00"><br><br>


<label for="lname">Entry No (find this in the more-info screen graph):</label><br>
  <input type="text" id="TeamEntry" name="Entry" value="3"><br><br>

  <label for="lname">Time: (correct time for that entry)</label><br>
  <input type="text" id="TeamNo" name="Time" value="1.111"><br><br>

  <label for="lname">Password:</label><br>
  <input type="password" id="s" name="pswd" value="0"><br><br>

  <input type="submit" value="Submit">
</form>

<p>Click Submit to continue</p>

</body>
</html>

"""
updateEntryHTML = updateEntryHTML.replace("$$$LEADERBOARD",preURL)



newTeamHTML = """<!DOCTYPE html>
<html>
<body>

<h2>New Team Registration:</h2>

<form action="$$$LEADERBOARD/NewTeamSubmit" method="POST">
    <h1> Team Details</h1>
    <label for="lname">Team Name: </label><br>
  <input type="text" id="TeamNo" name="name" value="team awesome"><br><br>

  <label for="lname">Members: (seperated by commas)</label><br>
  <input type="text" id="TeamNo" name="members" value="bob,sarah"><br><br>

 <label for="lname">Team Number: (Must be exact!)</label><br>
  <input type="text" id="TeamNo" name="teamNo" value="5"><br><br>

   <label for="lname">Year: (Must be exact!)</label><br>
  <input type="text" id="TeamNo" name="yrGroup" value="3W"><br><br>

  <label for="lname">Time: (leave 999 if haven't raced)</label><br>
  <input type="text" id="TeamNo" name="time" value="999"><br><br>

  <label for="lname">Password:</label><br>
  <input type="password" id="s" name="pswd" value="0"><br><br>

  <input type="submit" value="Submit">
</form>

<p>Click Submit to continue</p>

</body>
</html>

"""
newTeamHTML = newTeamHTML.replace("$$$LEADERBOARD",preURL)

updateTeamHTML = """<!DOCTYPE html>
<html>
<body>

<h2>Update Team Information:</h2>
<p1> check the existing stats first by opening the teamInfo page on the relevent class list. </p1>
<form action="$$$LEADERBOARD/updateTeamSubmit" method="POST">
    <h1> Team Details</h1>
    <label for="lname">Team Name: </label><br>
  <input type="text" id="TeamNo" name="name" value="teamNAME"><br><br>

  <label for="lname">Members: (seperated by commas)</label><br>
  <input type="text" id="TeamNo" name="members" value="mel,matt"><br><br>

 <label for="lname">Team Number: (Must be exact!)</label><br>
  <input type="text" id="TeamNo" name="teamNo" value="NULL"><br><br>

   <label for="lname">Year: (Must be exact!)</label><br>
  <input type="text" id="TeamNo" name="yrGroup" value="0X"><br><br>

  <label for="lname">Password:</label><br>
  <input type="password" id="s" name="pswd" value="0"><br><br>

  <input type="submit" value="Submit">
</form>

<p>Click Submit to continue</p>

</body>
</html>

"""
updateTeamHTML = updateTeamHTML.replace("$$$LEADERBOARD",preURL)


indexPage = css
indexPage +="""
<style>
a {color:#666688;}
</style>

<!--- CUSTOMISATION ZONE EDIT HERE --!>



<h1> F1 in Schools Year Leaderboards: </h1>
<!-- add/remove leaderboards here for wide filters (ie one term as in 6 shows 6W 6T 6L)

copy the following format:
    <a href='$$$LEADERBOARD/year/%TERM%/%TITLE%'>  %LINK DESCRIPTION </a><br>

replace %TERM% with the filter term (i.e. 6 for all classes with the number 6 in them)
replace %TITLE% with the DISPLAYED title of the leaderboard term 
replace %LINK DESCRIPTION% with the DISPLAYED text for the link.

--!>

<a href='$$$LEADERBOARD/year/6/Year 6'>  Year 6 Leaderboard </a><br>
<a href='$$$LEADERBOARD/year/4/Year 4'>  Year 4 Leaderboard </a><br>




<h2> Class Leaderboards: </h2>
<!-- add/remove leaderboards here for wide filters (ie one term as in 6 shows 6W 6T 6L)

copy the following format:
    <a href='$$$LEADERBOARD/class/%CLASS%'>  %LINK DESCRIPTION </a><br>

replace %CLASS% with the exact class name (i.e. 6W will only show entrys where class = 6W)
replace %TITLE% with the DISPLAYED title of the leaderboard term 
replace %LINK DESCRIPTION% with the DISPLAYED text for the link.

--!>

<a href='$$$LEADERBOARD/class/6W'>  6W Leaderboard </a><br>
<a href='$$$LEADERBOARD/class/6T'>  6T Leaderboard </a><br>
<a href='$$$LEADERBOARD/class/6L'>  6L Leaderboard </a><br>
<br>
<a href='$$$LEADERBOARD/class/4W'>  4W Leaderboard </a><br>
<a href='$$$LEADERBOARD/class/4T'>  4T Leaderboard </a><br>
<a href='$$$LEADERBOARD/class/4L'>  4L Leaderboard </a><br>


<!--- CUSTOMISATION ZONE ENDS! Don't edit any more unless you know what you are doing. --!>


<h2> New Entry: </h2>
<a href='$$$LEADERBOARD/newEntry'>   Create New Time Entry </a><br>
<a href='$$$LEADERBOARD/newTeam'>  Add Team </a>
<h2> Update Entries: </h2>
<a href='$$$LEADERBOARD/updateEntry'>   Edit Previous Time Entry </a><br>
<a href='$$$LEADERBOARD/updateTeam'>  Edit Team Information</a>
"""
indexPage = indexPage.replace("$$$LEADERBOARD",preURL)

##VIEWING LISTS


@app.route('/')
def index():
    return indexPage


@app.route('/year/<year>/<title>')
def yearList(year,title):
    output = css
    output += dbi.render(dbi.yearFilter(year),title)
    return output

@app.route('/class/<Class>')
def classList(Class):
    output = css
    output += dbi.render(dbi.classFilter(Class),Class)
    return output
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
        return 'Thankyou Click <a href="'+ preURL + '/newEntry"> Here </a> To go record another or: <a href="'+ preURL + '/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="'+ preURL + '/newEntry"> Here </a> To go try again'

@app.route('/NewTeamSubmit',methods=["POST"])
def newTeamForm():
    if int(request.form["pswd"]) == PSWD():
        members = request.form["members"].split(",")
        outMembers = []
        for i in members:
            outMembers.append(i.strip())
        dbi.newTeam(request.form["name"],outMembers,request.form["yrGroup"],request.form["teamNo"],request.form["time"])
        dbi.save()
        return 'Thankyou Click <a href="'+ preURL + '/NewTeamSubmit"> Here </a> To go record another or: <a href="'+ preURL + '"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="'+ preURL + '/newEntry"> Here </a> To go try again'
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
        return 'Click<a href="'+ preURL + '/"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="'+ preURL + '/updateEntry"> Here </a> To go try again'
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
        return 'Thankyou Click <a href="'+ preURL + '"> Here for main menu</a> '
    else:
        return 'Wrong Password! <a href="'+ preURL + '/updateEntry"> Here </a> To go try again'


### DEEEP INFO ON TEAMS
@app.route('/team/<teamNo>')
def moreInfo(teamNo):
    record = dbi.data[teamNo]
    output = css
    output += moreInfoHTML
    members = ", ".join(record['members'])
    output = output.replace("###NAME",record['name'])
    output = output.replace("###TEAMNO",teamNo)
    output = output.replace("###CLASS",record['class'])
    output = output.replace("###MEMBERS",members)
    output = output.replace("###FASTEST",str(record['fast']))
    ##TIMES
    timeList = []
    labelList = []
    counter = 1
    for i in record['times']:
        timeList.append(record['times'][i])
        labelList.append(counter)
        counter += 1
    output = output.replace("###TIMES_LIST",str(timeList))
    output = output.replace("###LABLES_LIST",str(labelList))



    return output

######## SEND IMAGES:
@app.route('/get_image/<name>')
def get_image(name):
    name = "img/"  + name
    return send_file(name, mimetype='image/gif')




if __name__ == '__main__':
    app.run(host='localhost',port='8000')
