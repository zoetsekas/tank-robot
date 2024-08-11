from pprint import pprint

import ray
from ray.rllib.algorithms import Algorithm
from ray.tune.logger import pretty_print
from ray.tune.registry import get_trainable_cls

from rl import env_cfg


def start_training_tank():
    config = (
        get_trainable_cls('PPO')
        .get_default_config()
        .environment(env="TankRoyale-v0", env_config=env_cfg)
        .training(
            train_batch_size=256,
            gamma=0.3,
            lr=0.001,
            # sgd_minibatch_size=64,
            # clip_param = 0.5,
            # vf_clip_param = 10.0,
            # kl_coeff=0,
            # entropy_coeff=1.0,
            # model={
            #     "use_lstm": False,
            #     # "lstm_use_prev_action": True,
            #     # "lstm_use_prev_reward": True,
            #     "fcnet_hiddens": [512, 256, 128, 64, 32],
            #     "fcnet_activation": "relu",
            # },
            # model={
            #     "use_attention": True,
            #     "max_seq_len": 10,
            #     "attention_num_transformer_units": 1,
            #     "attention_dim": 32,
            #     "attention_memory_inference": 10,
            #     "attention_memory_training": 10,
            #     "attention_num_heads": 1,
            #     "attention_head_dim": 32,
            #     "attention_position_wise_mlp_dim": 32,
            # },
        )
        # .framework(framework="tf2")
        .framework(framework="torch")
        # .framework(framework="tf2", eager_tracing=True)
        .resources(num_gpus=1, num_cpus_per_worker=12)
        # .rollouts(num_rollout_workers=0, num_envs_per_worker=1, preprocessor_pref=None)
        .rollouts(num_rollout_workers=0, num_envs_per_worker=1, preprocessor_pref=None)
        # .callbacks(callbacks_class=TensorboardCallback)
        .reporting(keep_per_episode_custom_metrics=True)
        # .evaluation(evaluation_interval=1, evaluation_duration=5, evaluation_duration_unit="episodes")
        .debugging(log_level="INFO")
    )

    pprint(config.to_dict())

    if ray.is_initialized():
        ray.shutdown()

    ray.init(logging_level=0, address='local', num_cpus=48, num_gpus=1, dashboard_port=8668, namespace='tank-royale',
             include_dashboard=False)

    algo: Algorithm = config.build()

    for i in range(env_cfg['max_episode_steps']):
        print(f"Episodes:{i}")
        result = algo.train()
        print(pretty_print(result))
        checkpoint_dir = algo.save()
        print(f"Checkpoint saved in directory {checkpoint_dir}")
    # algo.evaluate()
    algo.stop()
    # algo.load_checkpoint()
    ray.shutdown()
