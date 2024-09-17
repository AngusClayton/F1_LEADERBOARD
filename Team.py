class Team:
    #"5": {"name": "team awesome", "class": "3W", "members": ["bob", "sarah"], "times": {"1621481186": 999.0}, "fast": 999.0, "#": "5"}
    def __init__(self, name, members, yrGroup, no, RACEtime,times):
        self.name = name
        self.members = members
        self.yrGroup = yrGroup
        self.no = no
        self.fastest = RACEtime
        self.times = times
    def __str__(self):
        return f"Team {self.no}: {self.name} ({self.yrGroup}) 