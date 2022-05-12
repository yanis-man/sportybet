from .GlobalController import GlobalController

from datetime import datetime
from random import randint

class ApiController(GlobalController):
    def __init__(self):
        super().__init__()
    def populateTodayFixture(self):
        today = datetime.now()
        today_date = today.strftime("%Y-%m-%d")
        if len(self.database.pull_from_db(f"SELECT * FROM fixtures WHERE day = {today.day}")) == 0:
            # there's not any registered fixture today
            fixtures_list = self.api_url.get_fixture_list(today_date)
            for game in fixtures_list:
                game_odds = self.api_url.get_game_odds(game[0], today_date)
                game_date = game[6].split(',')
                query_params = (game[1], game[4], game_odds[0], game[5], game_odds[2], game_odds[1], f'{game_date[2]}-{ f"0{today.month}" if int(game_date[1]) < 10 else game_date[1] }-{game_date[0]}', f'{game_date[3]}:{game_date[4]}', game[0])
                self.database.save_to_db("INSERT INTO fixtures (league_name, team1_name, team1_odd, team2_name, team2_odd, drawn_odd, day, hour, uid) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)", query_params)

    
    def placeBet(self, data, user_id):
        totalOdd = float(data['globalOdd'])
        betAmount = int(data['betAmount'])
        #verifiy parameters
        if not (totalOdd > 0 and betAmount > 0):
            return 1
        self.database.save_to_db("INSERT INTO coupons (user_id, coupon_amount, coupon_odd, placed_date) VALUES (%s, %s, %s, NOW())", (user_id, betAmount, totalOdd))
        coupon_id = self.database.pull_from_db("SELECT id FROM coupons ORDER BY id DESC LIMIT 1;", only_first=True)[0]
        bets_id_list = data['betsList'] 
        for single_bet in bets_id_list:
            # fixture id : pred
            fixture_id, bet_pred = list(single_bet.items())[0]
            params = (coupon_id, bet_pred, fixture_id)
            self.database.save_to_db('INSERT INTO bets_placed (coupon_id, bet_pred, fixture_id) VALUES (%s, %s, %s)', params)
        
        self.database.save_to_db("UPDATE users SET balance = balance - %s WHERE id = %s", betAmount, user_id)