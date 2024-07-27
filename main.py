import os
import json
import time
import requests
import urllib.parse
from colorama import init, Fore
from getpass import getpass

init(autoreset=True)

class OKX:
    def __init__(self):
        self.session = requests.Session()

    def headers(self, query_id=None):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "App-Type": "web",
            "Content-Type": "application/json",
            "Origin": "https://www.okx.com",
            "Referer": "https://www.okx.com/mini-app/racer?tgWebAppStartParam=linkCode_85298986",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
            "X-Cdn": "https://www.okx.com",
            "X-Locale": "en_US",
            "X-Utc": "7",
            "X-Zkdex-Env": "0"
        }
        if query_id:
            headers['X-Telegram-Init-Data'] = query_id
        return headers

    def post_to_okx_api(self, ext_user_id, ext_user_name, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/info?t={int(time.time())}"
        payload = {
            "extUserId": ext_user_id,
            "extUserName": ext_user_name,
            "gameId": 1,
            "linkCode": "88910038"
        }
        response = self.session.post(url, json=payload, headers=self.headers(query_id))
        return response.json()

    def assess_prediction(self, ext_user_id, predict, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/assess?t={int(time.time())}"
        payload = {
            "extUserId": ext_user_id,
            "predict": predict,
            "gameId": 1
        }
        response = self.session.post(url, json=payload, headers=self.headers(query_id))
        return response.json()

    def check_daily_rewards(self, ext_user_id, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/tasks?t={int(time.time())}"
        try:
            response = self.session.get(url, headers=self.headers(query_id))
            tasks = response.json().get('data', [])
            daily_check_in_task = next((task for task in tasks if task['id'] == 4), None)
            if daily_check_in_task:
                if daily_check_in_task['state'] == 0:
                    self.log('Start checkin ... ')
                    self.perform_check_in(ext_user_id, daily_check_in_task['id'], query_id)
                else:
                    self.log('Today you have attended!')
        except Exception as e:
            self.log(f"Daily reward check error: {e}")

    def perform_check_in(self, ext_user_id, task_id, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/task?t={int(time.time())}"
        payload = {
            "extUserId": ext_user_id,
            "id": task_id
        }
        try:
            self.session.post(url, json=payload, headers=self.headers(query_id))
            self.log('Daily attendance successfully!')
        except Exception as e:
            self.log(f"Error: {e}")

    def log(self, msg):
        print(f"[*] {msg}")

    def sleep(self, seconds):
        time.sleep(seconds)

    def wait_with_countdown(self, seconds):
        for i in range(seconds, -1, -1):
            print(f"\r===== Completed all accounts, waiting {i} seconds to continue the loop =====", end='', flush=True)
            time.sleep(1)
        print('')

    def countdown(self, seconds):
        for i in range(seconds, -1, -1):
            print(f"\r[*] Wait {i} Seconds to continue ...", end='', flush=True)
            time.sleep(1)
        print('')

    def extract_user_data(self, query_id):
        url_params = urllib.parse.parse_qs(query_id)
        user = json.loads(urllib.parse.unquote(url_params.get('user')[0]))
        return {
            'extUserId': user['id'],
            'extUserName': user['username']
        }

    def get_boosts(self, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/boosts?t={int(time.time())}"
        try:
            response = self.session.get(url, headers=self.headers(query_id))
            return response.json().get('data', [])
        except Exception as e:
            self.log(f"BOOSTS Information Error: {e}")
            return []

    def use_boost(self, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t={int(time.time())}"
        payload = {'id': 1}
        try:
            response = self.session.post(url, json=payload, headers=self.headers(query_id))
            if response.json().get('code') == 0:
                self.log(Fore.YELLOW + 'Reload Fuel Tank successfully!')
                self.countdown(5)
            else:
                self.log(Fore.RED + f"Error Reload Fuel Tank: {response.json().get('msg')}")
        except Exception as e:
            self.log(Fore.RED + f"Crazyi: {e}")

    def upgrade_fuel_tank(self, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t={int(time.time())}"
        payload = {'id': 2}
        try:
            response = self.session.post(url, json=payload, headers=self.headers(query_id))
            if response.json().get('code') == 0:
                self.log(Fore.YELLOW + 'Upgrade Fuel Tank success!')
            else:
                self.log(Fore.RED + f"Upgrade error Fuel Tank: {response.json().get('msg')}")
        except Exception as e:
            self.log(Fore.RED + f"Crazyi: {e}")

    def upgrade_turbo(self, query_id):
        url = f"https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t={int(time.time())}"
        payload = {'id': 3}
        try:
            response = self.session.post(url, json=payload, headers=self.headers(query_id))
            if response.json().get('code') == 0:
                self.log(Fore.YELLOW + 'Successful Turbo Charger upgrade!')
            else:
                self.log(Fore.RED + f"Turbo Charge upgrade errorr: {response.json().get('msg')}")
        except Exception as e:
            self.log(Fore.RED + f"Error: {e}")

    def ask_question(self, query):
        return input(query)

    def main(self):
        data_file = os.path.join(os.path.dirname(__file__), 'data.txt')
        with open(data_file, 'r', encoding='utf8') as file:
            user_data = [line.strip() for line in file if line.strip()]

        nangcapfueltank = self.ask_question('Do you want to upgrade Fuel Tank? (y/n): ')
        hoinangcap = nangcapfueltank.lower() == 'y'
        nangcapturbo = self.ask_question('Do you want to upgrade Turbo Charger? (y/n): ')
        hoiturbo = nangcapturbo.lower() == 'y'

        while True:
            for query_id in user_data:
                user_info = self.extract_user_data(query_id)
                ext_user_id = user_info['extUserId']
                ext_user_name = user_info['extUserName']
                try:
                    self.check_daily_rewards(ext_user_id, query_id)

                    boosts = self.get_boosts(query_id)
                    for boost in boosts:
                        self.log(Fore.GREEN + f"{boost['context']['name']}: {boost['curStage']}/{boost['totalStage']}")
                    reload_fuel_tank = next((boost for boost in boosts if boost['id'] == 1), None)
                    fuel_tank = next((boost for boost in boosts if boost['id'] == 2), None)
                    turbo = next((boost for boost in boosts if boost['id'] == 3), None)

                    if fuel_tank and hoinangcap:
                        balance_response = self.post_to_okx_api(ext_user_id, ext_user_name, query_id)
                        balance_points = balance_response['data']['balancePoints']
                        if fuel_tank['curStage'] < fuel_tank['totalStage'] and balance_points > fuel_tank['pointCost']:
                            self.upgrade_fuel_tank(query_id)
                            boosts = self.get_boosts(query_id)
                            updated_fuel_tank = next((boost for boost in boosts if boost['id'] == 2), None)
                            updated_balance_points = self.post_to_okx_api(ext_user_id, ext_user_name, query_id)['data']['balancePoints']
                            if updated_fuel_tank['curStage'] >= fuel_tank['totalStage'] or updated_balance_points < fuel_tank['pointCost']:
                                self.log(Fore.RED + 'Not eligible to upgrade Fuel Tank!')
                                continue
                        else:
                            self.log(Fore.RED + 'Not eligible to upgrade Fuel Tank!')

                    if turbo and hoiturbo:
                        balance_response = self.post_to_okx_api(ext_user_id, ext_user_name, query_id)
                        balance_points = balance_response['data']['balancePoints']
                        if turbo['curStage'] < turbo['totalStage'] and balance_points > turbo['pointCost']:
                            self.upgrade_turbo(query_id)
                            boosts = self.get_boosts(query_id)
                            updated_turbo = next((boost for boost in boosts if boost['id'] == 3), None)
                            updated_balance_points = self.post_to_okx_api(ext_user_id, ext_user_name, query_id)['data']['balancePoints']
                            if updated_turbo['curStage'] >= turbo['totalStage'] or updated_balance_points < turbo['pointCost']:
                                self.log(Fore.RED + 'Upgrading Turbo Charger failed!')
                                continue
                        else:
                            self.log(Fore.RED + 'Not eligible to upgrade Turbo Charger!')

                    for _ in range(50):
                        response = self.post_to_okx_api(ext_user_id, ext_user_name, query_id)
                        balance_points = response['data']['balancePoints']
                        self.log(Fore.GREEN + f"balancePoints: {balance_points}")

                        predict = 1
                        assess_response = self.assess_prediction(ext_user_id, predict, query_id)
                        assess_data = assess_response['data']
                        result = Fore.GREEN + 'Win' if assess_data['won'] else Fore.RED + 'Lose'
                        calculated_value = assess_data['basePoint'] * assess_data['multiplier']
                        self.log(Fore.MAGENTA + f"Result: {result} x {assess_data['multiplier']}! Balance: {assess_data['balancePoints']}, Receive: {calculated_value}, Old price: {assess_data['prevPrice']}, Current price: {assess_data['currentPrice']}")

                        if assess_data['numChance'] <= 0 and reload_fuel_tank and reload_fuel_tank['curStage'] < reload_fuel_tank['totalStage']:
                            self.use_boost(query_id)
                            boosts = self.get_boosts(query_id)
                            reload_fuel_tank = next((boost for boost in boosts if boost['id'] == 1), None)
                        elif assess_data['numChance'] > 0:
                            self.countdown(5)
                            continue
                        elif assess_data['secondToRefresh'] > 0:
                            self.countdown(assess_data['secondToRefresh'] + 5)
                        else:
                            break

                except Exception as e:
                    self.log(Fore.RED + f"Error: {e}")

            self.wait_with_countdown(60)

if __name__ == "__main__":
    okx = OKX()
    try:
        okx.main()
    except Exception as e:
        print(Fore.RED + str(e))
        exit(1)