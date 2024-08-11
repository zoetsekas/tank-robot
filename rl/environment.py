from typing import Any, Tuple, Dict, SupportsFloat

import gymnasium
import gymnasium as gym
from gymnasium.core import ObsType, ActType
from gymnasium.spaces import Discrete

from rl.robocode import RoboCodeController


class RoboCode(gym.Env):

    def __init__(self, env_config: dict):
        super().__init__()
        self.config = env_config
        seed = env_config['seed']

        # https://github.com/robocode-dev/tank-royale/blob/main/schema/schemas/bot-intent.yaml
        '''
                value = 720
            turnRate (value-360), gunTurnRate(value-360), radarTurnRate(value-360)
                value = 400
            targetSpeed(value-200)
            firepower (0-3)
        '''
        self.action_space = gymnasium.spaces.Dict(
            {
                "turnRate": Discrete(n=360, start=-180, seed=seed),
                "gunTurnRate": Discrete(n=360, start=-180, seed=seed),
                "radarTurnRate": Discrete(n=360, start=-180, seed=seed),
                "targetSpeed": Discrete(n=200, start=-100, seed=seed),
                "firepower": Discrete(n=4, start=0, seed=seed),
            }
        )

        '''
            Bot related information
                * energy(0-400), x, y, direction(0-360), gunDirection(0-360), radarDirection(0-360),
                * radarSweep(0-180), speed(0-400), turnRate(value-360), gunTurnRate(value-360),
                * radarTurnRate(value-360), gunHeat(0-200)
            
            Bullet related information
                * power(0-3), x, y, direction, 
        '''
        self.observation_space = gymnasium.spaces.Dict(
            {
                "bot": gymnasium.spaces.Dict(
                    {
                        "energy": Discrete(n=400, start=0, seed=seed),
                        "x": Discrete(n=1000, start=0, seed=seed),
                        "y": Discrete(n=1000, start=0, seed=seed),
                        "direction": Discrete(n=360, start=-180, seed=seed),
                        "gunDirection": Discrete(n=360, start=-180, seed=seed),
                        "radarDirection": Discrete(n=360, start=-180, seed=seed),
                        "radarSweep": Discrete(n=180, start=0, seed=seed),
                        "speed": Discrete(n=180, start=0, seed=seed),
                        "turnRate": Discrete(180),
                        "gunTurnRate": Discrete(720),
                        "radarTurnRate": Discrete(720),
                        "gunHeat": Discrete(n=200, start=0, seed=seed),

                    }
                ),
                "bullet": gymnasium.spaces.Dict(
                    {
                        "power": Discrete(n=4, start=0, seed=seed),
                        "x": Discrete(n=1000, start=0, seed=seed),
                        "y": Discrete(n=1000, start=0, seed=seed),
                        "direction": Discrete(360),
                    }
                )
            }
        )

        self._spaces_in_preferred_format = True
        self._action_space_in_preferred_format = True
        self._obs_space_in_preferred_format = True

        # self._skip_env_checking = True
        self.timestep = 0
        self.last_tick_event_for_bot = None
        self.buffer = []
        self.terminated = False
        self.truncated = False
        print("Initializing Environment")

        self.controller = RoboCodeController(callback_on_message=self.callback)

    def callback(self, message):

        if message['type'] == 'TickEventForBot':
            self.last_tick_event_for_bot = message
        elif message['type'] == 'RoundEndedEvent':
            self.truncated = True
        elif message['type'] in ['GameAbortedEvent', 'GameEndedEventForBot', 'BotDeathEvent']:
            self.terminated = True
        else:
            self.buffer.append(message)

    def step(self, action: ActType) -> Tuple[ObsType, SupportsFloat, bool, bool, Dict[str, Any]]:

        # Send actions to RoboCode server

        # Process observations and set reward accordingly
        # get Observations from RoboCode server
        obs = self.last_tick_event_for_bot

        # TODO
        rew = 1

        self.timestep += 1
        self.buffer = []

        return obs, rew, self.terminated, self.truncated, {}

    def reset(self, *, seed: int = None, options: Dict[str, Any] = None) \
            -> Tuple[ObsType, Dict[str, Any]]:

        self.timestep = 0
        self.last_tick_event_for_bot = None
        self.buffer = []
        self.terminated = False
        self.truncated = False

        return self.last_tick_event_for_bot, {}

    def get_observations(self):
        event = self.last_tick_event_for_bot


if __name__ == '__main__':

    env_cfg = {
        'max_episode_steps': 10,
    }

    tank = RoboCode(env_config=env_cfg)
    while True:
        action_temp = tank.action_space.sample()
        tank.step(action=action_temp)
