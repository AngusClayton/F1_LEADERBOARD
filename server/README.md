# F1_LEADERBOARD SERVER

A intuitive leader board system designed for in school use, sorting times by class and year group.

## Pre-requites

Python 3.X (tested on 3.6.9 *nice*)

python3 flask

## Setup

The project comes with some sample data ***note: all data is stored in data.json*** 

To start fresh; delete the contents of **data.json**, and replace with:

 `{}`

You can also reset times, but not teams by running the **reset.py** script.

## Customisation:

### Custom Filters 

<u>(adding own year groups and classes)</u>

To add a custom filter, you will need to edit *approx.* **line 246 - 289**

i.e. between:**

`<!--- CUSTOMISATION ZONE EDIT HERE --!>`

***and***

`<!--- CUSTOMISATION ZONE ENDS! Don't edit any more unless you know what you are doing. --!>`

T

#### Adding a year group sort:

Insert the following lines; best U.I. placement is under the `customization zone edit here` comment

`<!-- add/remove leaderboards here for wide filters (ie one term as in 6 shows 6W 6T 6L)`



`copy the following format:`

    `<a href='$$$LEADERBOARD/year/%TERM%/%TITLE%'>  %LINK DESCRIPTION </a><br>`



`replace %TERM% with the filter term (i.e. 6 for all classes with the number 6 in them)`

`replace %TITLE% with the DISPLAYED title of the leaderboard term` 

`replace %LINK DESCRIPTION% with the DISPLAYED text for the link.`



`--!>`

#### Adding A Class group sort:

Insert the following lines; best U.I. placement is under the `<h2> class Leader boards: </h2>` line.

`<!-- add/remove leaderboards here for wide filters (ie one term as in 6 shows 6W 6T 6L)`



`copy the following format:`

    `<a href='$$$LEADERBOARD/class/%CLASS%'>  %LINK DESCRIPTION </a><br>`



`replace %CLASS% with the exact class name (i.e. 6W will only show entrys where class = 6W)`

`replace %TITLE% with the DISPLAYED title of the leaderboard term` 

`replace %LINK DESCRIPTION% with the DISPLAYED text for the link.`



`--!>`

### Using with a reverse proxy.

You can use this flask script with a reverse proxy, to map a URL on your web server to the port 8000. 

*However* this will cause issues with all the URLs, as the have an extra directory(s) in them.

You can add these to the front of **ALL LINKS** by editing the **preURL** variable present in the beginning of **both main.py AND dbi.py files.**

<u>You must edit both or it will not work.</u>

## 