# import gymnasium as gym
# from ray.rllib.env import EnvContext
# from ray.rllib.utils import check_env
# from ray.tune import register_env
#
# from rl.environment import RoboCode
#
# env_cfg = {
#     'max_episode_steps': 10,
# }
#
# gym.envs.register(
#     id='TankRoyale-v0',
#     entry_point='rl.environment:RoboCode',
#     disable_env_checker=True,
#     max_episode_steps=env_cfg['max_episode_steps'],
#     kwargs={"env_config": env_cfg},
# )
#
#
# def check_environment():
#     # How to check you do not have any environment errors
#     print("checking environment ...")
#     try:
#         check_env(RoboCode(env_config=EnvContext(env_config=env_cfg, worker_index=0)))
#         print("All checks passed. No errors found.")
#     except ValueError as e:
#         print("failed")
#
#
# def env_creator(cfg):
#     return RoboCode(env_config=EnvContext(env_config=cfg, worker_index=0))
#
#
# register_env('TankRoyale-v0', env_creator)
