import json
import os
import random
import rel as rel
import websocket
import yaml
from dotenv import load_dotenv
from websocket import WebSocketApp
from colorama import Fore, Back, Style
import subprocess

load_dotenv(dotenv_path='/app/.env')


def check_ping(hostname: str) -> bool:
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        status = True
    else:
        status = False

    return status


class RoboCodeController:

    def __init__(self, callback_on_message, mode: str):
        self.callback_on_message = callback_on_message
        self.mode = mode
        self.joined_bots = 0

        # host = None
        # local_hostname = os.getenv('server_address')
        # if check_ping(local_hostname):
        #     host = local_hostname
        # else:

        # host = '172.20.0.2'
        host = 'tank-gui-app'
        # host = 'tank-server-app'
        if check_ping(host):
            print("Successfully connected to " + host)
        # host = 'localhost'
        # host = 'tank-server-app'
        # host = os.getenv('server_address')
        connection = f"ws://{host}:{os.getenv('server_port')}"
        print(f"Starting websocket: {connection}")
        self.ws = websocket.WebSocketApp(connection,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        self.ws.run_forever(dispatcher=rel, reconnect=5)
        rel.signal(2, rel.abort)
        rel.dispatch()

    def tick_event_for_bot(self, connection, message):
        print(f'tick_event_for_bot:{message}')
        handshake: dict = {
            'sessionId': message['sessionId'],
            'name': os.getenv('name'),
            'version': os.getenv('version'),
            'authors': os.getenv('authors').split(","),
            'type': 'BotHandshake',
            'secret': os.getenv('secret'),
        }
        data = json.dumps(handshake)
        connection.send(data)

    def skipped_turn_event(self, connection, message):
        print(f'skipped_turn_event:{message}')

    def round_ended_event(self, connection, message):
        print(f'round_ended_event:{message}')

    def bot_intent(self, connection, message):
        print(f'bot_intent:{message}')

    def bot_death_event(self, connection, message):
        print(f'bot_death_event:{message}')

    def bot_hit_event(self, connection, message):
        print(f'bot_hit_event:{message}')

    def bot_hit_wall_event(self, connection, message):
        print(f'bot_hit_wall_event:{message}')

    def bullet_fired_event(self, connection, message):
        print(f'bullet_fired_event:{message}')

    def bullet_hit_bot_event(self, connection, message):
        print(f'bullet_hit_bot_event:{message}')

    def scanned_bot_event(self, connection, message):
        print(f'scanned_bot_event:{message}')

    def hit_by_bullet_event(self, connection, message):
        print(f'hit_by_bullet_event:{message}')

    def bullet_hit_wall_event(self, connection, message):
        print(f'bullet_hit_wall_event:{message}')

    def bullet_hit_bullet_event(self, connection, message):
        print(f'bullet_hit_bullet_event:{message}')

    def bot_list_update(self, connection, message):
        print(f'bot_list_update:{message}')
        self.joined_bots = len(message['bots'])
        print(f'bots number:{self.joined_bots}')

    # https://github.com/robocode-dev/tank-royale/blob/master/schema/schemas/README.md
    def on_message(self, connection, message):
        message = json.loads(message)

        self.callback_on_message(message)

        if message['type'] == 'ServerHandshake':
            self.server_handshake(connection, message)
        elif message['type'] == 'GameStartedEventForBot':
            self.game_started_event_for_bot(connection)
        elif message['type'] == 'RoundStartedEvent':
            self.round_started_event(connection, message)
        elif message['type'] == 'RoundEndedEvent':
            self.round_ended_event(connection, message)
        elif message['type'] == 'TickEventForBot':
            self.tick_event_for_bot(connection, message)
        elif message['type'] == 'SkippedTurnEvent':
            self.skipped_turn_event(connection, message)
        elif message['type'] == 'BotDeathEvent':
            self.bot_death_event(connection, message)
        elif message['type'] == 'BotHitBotEvent':
            self.bot_hit_event(connection, message)
        elif message['type'] == 'BotHitWallEvent':
            self.bot_hit_wall_event(connection, message)
        elif message['type'] == 'BulletFiredEvent':
            self.bullet_fired_event(connection, message)
        elif message['type'] == 'BulletHitBotEvent':
            self.bullet_hit_bot_event(connection, message)
        elif message['type'] == 'BulletHitBulletEvent':
            self.bullet_hit_bullet_event(connection, message)
        elif message['type'] == 'BulletHitWallEvent':
            self.bullet_hit_wall_event(connection, message)
        elif message['type'] == 'HitByBulletEvent':
            self.hit_by_bullet_event(connection, message)
        elif message['type'] == 'ScannedBotEvent':
            self.scanned_bot_event(connection, message)
        elif message['type'] == 'BotListUpdate':
            self.bot_list_update(connection, message)

        else:
            print(f"---- message not processed: {message['type']}")

    def server_handshake(self, connection: WebSocketApp, message):

        print(f'server_handshake:{message}')
        handshake: dict = {}
        if self.mode == "Bot":
            handshake: dict = {
                'sessionId': message['sessionId'],
                'name': os.getenv('name'),
                'version': os.getenv('version'),
                'authors': os.getenv('authors').split(","),
                'type': 'BotHandshake',
                'secret': os.getenv('bot_secret'),
            }
        elif self.mode == "Controller":
            handshake: dict = {
                'sessionId': message['sessionId'],
                'name': 'Controller',
                'variant': 'Tank Royale',
                'version': os.getenv('version'),
                'type': 'ControllerHandshake',
                'gameTypes': ['classic', '1v1', 'melee', 'custom'],
                'secret': os.getenv('controller_secret'),
            }
        data = json.dumps(handshake)
        connection.send(data)

    @staticmethod
    def game_started_event_for_bot(connection: WebSocketApp):
        data = {
            'type': 'BotReady'
        }
        connection.send(json.dumps(data))

    @staticmethod
    def round_started_event(connection: WebSocketApp, message):
        pass

    def on_error(self, ws, error):
        print(f'error: {error}')

    def on_close(self, ws, close_status_code, close_msg):
        print(f"### closed ### -- status code: {close_status_code} -- message: {close_msg}")

    def on_open(self, ws):
        print("Opening connection...")
        ws.send(self.start_server_handshake())

    @staticmethod
    def start_server_handshake():
        handshake: dict = {
            'sessionId': random.randrange(1, 100),
            'variant': os.getenv('variant'),
            'version': os.getenv('version'),
            'gameTypes': os.getenv('gameTypes'),
            'type': 'ServerHandshake',
        }
        return handshake


def callback(message):
    print(message)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # subprocess.Popen(['java', '-jar', 'robocode-tankroyale-gui-0.19.2.jar'], cwd='/app/robocode/')
    # subprocess.Popen(['java', '-jar', 'robocode-tankroyale-booter-0.19.2.jar', 'run', '/app/bots/Target'],
    #                  cwd='/app/robocode/')

    controller = RoboCodeController(callback_on_message=callback, mode='Controller')
    bot = RoboCodeController(callback_on_message=callback, mode='Bot')
