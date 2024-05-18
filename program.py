preset_entries = {
    "Washburn Rural": 0,
    "Blue Valley Southwest": 0,
    "Andover": 0,
    "Blue Valley North": 0,
    "Lawrence Free State": 0,
    "Blue Valley West": 0,
    "Greenhill Fall Classic": 0,
    "Mid America Cup (Valley)": 0,
    "Trevian Invitational (New Trier)": 0,
    "Heart of Texas (St Marks)": 0,
    "JW Patterson Invitational (Heritage Hall)": 0,
    "Iowa Caucus": 0
}
preset_prelims = {
    "Washburn Rural": 6,
    "Blue Valley Southwest": 6,
    "Andover": 5,
    "Blue Valley North": 5,
    "Lawrence Free State": 5,
    "Blue Valley West": 5,
    "Greenhill Fall Classic": 6,
    "Mid America Cup (Valley)": 6,
    "Trevian Invitational (New Trier)": 6,
    "Heart of Texas (St Marks)": 6,
    "JW Patterson Invitational (Heritage Hall)": 6,
    "Iowa Caucus": 6
}
elims_weights = {
    0: 1,
    1: 1.1,
    2: 1.2,
    3: 1.4,
    4: 1.6,
    5: 1.8,
    6: 2.3
}

class Tournament:
    def __init__(self, name: str, entries: str, prelimCount: str, prelimLosses: str, elimCount: str) -> None:
        self.name : str = name
        self.prelimLosses : int = int(prelimLosses)
        self.elimCount : int = int(elimCount)

        if name != "Other":
            self.entries = preset_entries[name]
            self.prelimCount = preset_prelims[name]
        else:
            self.entries = int(entries)
            self.prelimCount = int(prelimCount)
    
    def GetScore(self) -> float:
        return self.entries * ((self.prelimCount - self.prelimLosses) / self.prelimCount) * (elims_weights[self.elimCount])

class Team:
    def __init__(self, data: list[str]) -> None:
        self.data : list[str] = data
        self.code : str = data[2]
        self.tournaments : list[Tournament] = []
        self.score : float = 0.0

        for i in range(3,len(data),5):
            if (self.data[i] == "" or self.data[i] == "\n"): 
                continue
            self.tournaments.append(Tournament(self.data[i], self.data[i+1], self.data[i+2], self.data[i+3], self.data[i+4]))
    
    def CalculateScore(self) -> None:
        for tournament in self.tournaments:
            self.score += tournament.GetScore()
        self.score /= len(self.tournaments)
    
    def __str__(self):
        return self.code

file = open("KCKCCRankingData.csv", "r")
teams : list[Team] = []
line_count = 0

for line in file:
    line_count += 1
    if line_count == 1: continue
    teams.append(Team(line.split(",")))

file.close()

for team in teams:
    team.CalculateScore()

teams.sort(key=lambda team: team.score, reverse=True)

file = open("KCKCCPresetRanks.txt", "w")

for i in range(len(teams)):
    file.write(f"{i+1}.\t {teams[i].code}\n")

file.close()
