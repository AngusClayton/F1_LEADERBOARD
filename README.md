# F1_LEADERBOARD SYSTEM

# Database
SQL database utalizing sqlite3
```
CREATE TABLE teams (
    id INTEGER PRIMARY KEY,    -- Corresponds to the "#" in the JSON
    name VARCHAR(255),         -- Team name
    class VARCHAR(10),         -- Class (e.g., "6L", "3W")
    members VARCHAR(255)       -- Team members (CSV) 
    
);

CREATE TABLE times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,           -- Foreign key linking to the 'teams' table
    time_record FLOAT,         -- The recorded time (e.g., 999.0)
    FOREIGN KEY (team_id) REFERENCES teams(id)
);
```
## Example data
```
INSERT INTO teams (id, name, class,  members) 
VALUES (5, 'team 5', '3W',  'Angus, Brian');

INSERT INTO times (team_id, time_record) VALUES (5, 2.543), (5,2.2341), (5,2.644), (5,2.24), (5,1.53);
```