import argparse
import subprocess
from enum import Enum, EnumMeta

from dotenv import load_dotenv

from rl.robocode import RoboCodeController, callback

load_dotenv(dotenv_path='/app/.env')
parser = argparse.ArgumentParser(prog='Robo code trainer',
                                 description='Trains a tank using Reinforcement Learning',
                                 epilog='Use actions to start training or inference')


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Action(str, Enum, metaclass=MetaEnum):
    TRAIN = 'train'
    GUI = 'gui'
    SERVER = 'server'
    CONTROLLER = 'controller'
    BOT = 'bot'
    PLAY = 'play'


if __name__ == '__main__':
    parser.add_argument('--action', type=Action, required=True, default='train')
    args = parser.parse_args()

    print(f'Action: {args.action}')

    if args.action == Action.TRAIN:
        RoboCodeController(callback_on_message=callback, mode='Bot')
    elif args.action == Action.GUI:
        subprocess.call(['java', '-jar', 'robocode-tankroyale-gui-0.24.1.jar'], cwd='/app/robocode/')
    elif args.action == Action.SERVER:
        subprocess.call(['java', '-jar', 'robocode-tankroyale-server-0.24.1.jar',
                         '--games=classic,melee',
                         '--port=7654',
                         '--controller-secrets=Jwxwdd5V1QN1ySWIpv0UsQ',
                         '--bot-secrets=wNzRU2AEwjsL1PFaZiM7lg'],
                        cwd='/app/robocode/')
    elif args.action == Action.BOT:
        subprocess.call(['java', '-jar', 'robocode-tankroyale-booter-0.24.1.jar', 'run', '/app/bots/Target'], cwd='/app/robocode/')
    elif args.action == Action.CONTROLLER:
        RoboCodeController(callback_on_message=callback, mode='Controller')
    else:
        pass
