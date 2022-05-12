import requests
import re
FOLLOWED_LEAGUES = [36,31,8,34,11,5,16,23]
# 36 : Premier League | 31 : La Liga | 8 : Bundesliga
# 34 ! Serie A       | 11 : Ligue 1 |  5 : D1 Belge
# 16 : D1 Hollandaise| 23! Portugal D1 | 
#

class DataApi:
    def get_fixture_list(self, date):
        # A[1]=[2135999,39,29865,8415,'Cancun FC','CSyD Dorados de Sinaloa','2022,0,18,23,00,00',-1,1,2,1,2,1,0,1,2,'7','8','','',43,'','',6,1];
        # 0: ID, 1: League, .., .., 4: T1, 5: T2, 6: DATE_TIME
        raw_fixtures = requests.get(f'https://www.nowgoal5.com/AjaxCenter/GetScheduleWithTimeZone.aspx?date={date}&order=time&timezone=1').text
        if len(raw_fixtures) < 0:
            return []
        fixtures_array = []
        # 0: league ID, 1: league name
        today_followed_leagues = {}
        raw_fixtures = raw_fixtures.split(";")

        # gets the match count from the raw text
        match_count = int(re.search("[0-9]+", raw_fixtures[0]).group(0))
        followed_leagues = FOLLOWED_LEAGUES

        # computes the index of followed leagues in today fetch
        for league in raw_fixtures[5+match_count-1:]:
            splited_league = league.split("=")
            if len(splited_league) < 2:
                # we no longer are into a league
                break
            parsed_league = eval(splited_league[1]) # parses the second part of the B[XX] = []
            if parsed_league[0] in followed_leagues and len(followed_leagues) > 0:
                # the league is followed and there's still leagues to be computed
                followed_leagues.remove(parsed_league[0])
                today_league_id = int(re.search("[0-9]+", splited_league[0]).group(0))

                today_followed_leagues[today_league_id] = parsed_league[2]


        for game in raw_fixtures[5:match_count-1]:
            parsed_line = eval(game.split("=")[1])
            if parsed_line[1] in today_followed_leagues.keys():
                # sets a user-friendly league's display name
                parsed_line[1] = today_followed_leagues.get(parsed_line[1])
                fixtures_array.append(parsed_line)
        
        return fixtures_array

    
    def get_game_odds(self, game_uid, date):
        odds_raw = requests.get(f"https://www.nowgoal5.com/Ajax.aspx?type=23&id={game_uid}&p={date}").text
        if len(odds_raw) > 0:
            odds = odds_raw.split(";")[2].split(',')[:3]
        else:
            odds = [0,0,0]
        return odds

    def get_game_score(self, game_uid, date):
        raw_score = requests.get(f'https://www.nowgoal5.com/Ajax.aspx?type=24&id={game_uid}&p={date}').text
        splitted_score = raw_score.split("-")
        if splitted_score[0] > splitted_score[1]:
            return 1
        elif splitted_score[0] < splitted_score[1]:
            return 2
        else:
            return 0

        # 1 : first team
        # 2 : second team
        # 0 : drawn