import os
import gc
import numpy as np
import gymnasium as gym
import highway_env
import imageio.v2 as imageio

from PIL import Image, ImageDraw, ImageFont
from stable_baselines3 import PPO
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.monitor import Monitor


os.makedirs("videos", exist_ok=True)

FPS = 10
MAX_STEPS = 300   # about 30 seconds


class VehicleOcclusionWrapper(gym.ObservationWrapper):
    def __init__(self, env, occlusion_prob=0.95):
        super().__init__(env)
        self.occlusion_prob = occlusion_prob

    def observation(self, obs):
        obs = obs.copy()
        if np.random.rand() < self.occlusion_prob:
            if len(obs.shape) == 2:
                obs[1:, :] = 0
        return obs


def make_video_env(
    vehicle_occlusion=False,
    occlusion_prob=0.95,
    vehicles_count=25,
    duration=80,
    seed=0
):
    env = gym.make("highway-v0", render_mode="rgb_array")

    env.unwrapped.config["vehicles_count"] = vehicles_count
    env.unwrapped.config["duration"] = duration
    env.unwrapped.config["simulation_frequency"] = 10
    env.unwrapped.config["policy_frequency"] = 2
    env.unwrapped.config["lanes_count"] = 4

    if vehicle_occlusion:
        env = VehicleOcclusionWrapper(env, occlusion_prob=occlusion_prob)

    env = Monitor(env)
    env.reset(seed=seed)

    return env


def add_overlay(frame, title, subtitle, step, border_color):
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)

    w, h = img.size

    # top panel
    panel_h = 42
    draw.rectangle([0, 0, w, panel_h], fill=(0, 0, 0))

    # colored border
    border = 6
    draw.rectangle([0, 0, w - 1, h - 1], outline=border_color, width=border)

    # text
    draw.text((12, 6), title, fill=(255, 255, 255))
    draw.text((12, 24), subtitle, fill=border_color)

    # timestep
    draw.text((w - 120, 12), f"Step: {step}", fill=(255, 255, 255))

    return np.array(img)


def record_video(
    model,
    env,
    path,
    title,
    subtitle,
    border_color,
    recurrent=False,
    max_steps=MAX_STEPS,
    fps=FPS
):
    writer = imageio.get_writer(path, fps=fps)
    obs, info = env.reset()

    if recurrent:
        lstm_states = None
        episode_starts = np.ones((1,), dtype=bool)

    try:
        for step in range(max_steps):
            frame = env.render()

            frame = add_overlay(
                frame,
                title=title,
                subtitle=subtitle,
                step=step,
                border_color=border_color
            )

            writer.append_data(frame)

            if recurrent:
                action, lstm_states = model.predict(
                    obs,
                    state=lstm_states,
                    episode_start=episode_starts,
                    deterministic=True,
                )
                episode_starts = np.array([False], dtype=bool)
            else:
                action, _ = model.predict(obs, deterministic=True)

            obs, reward, terminated, truncated, info = env.step(action)

            if terminated or truncated:
                break

    finally:
        writer.close()
        env.close()
        gc.collect()

    print(f"Saved: {path}")


print("Loading models...")

ppo_clean = PPO.load("models/ppo_clean.zip", device="cpu")
ppo_noise = PPO.load("models/ppo_noise.zip", device="cpu")
ppo_extreme = PPO.load("models/ppo_extreme_occlusion.zip", device="cpu")
recurrent_extreme = RecurrentPPO.load(
    "models/recurrent_ppo_extreme_occlusion.zip",
    device="cpu"
)

print("Models loaded successfully.")


# =====================================================
# VIDEO 1: PPO CLEAN
# =====================================================

env = make_video_env(
    vehicle_occlusion=False,
    vehicles_count=18,
    duration=80,
    seed=101
)

record_video(
    model=ppo_clean,
    env=env,
    path="videos/01_PPO_Clean_Driving.mp4",
    title="PPO Baseline",
    subtitle="Clean Highway Environment",
    border_color=(0, 180, 255),
    recurrent=False
)


# =====================================================
# VIDEO 2: PPO GAUSSIAN NOISE
# =====================================================

env = make_video_env(
    vehicle_occlusion=False,
    vehicles_count=24,
    duration=80,
    seed=202
)

record_video(
    model=ppo_noise,
    env=env,
    path="videos/02_PPO_Gaussian_Noise.mp4",
    title="PPO with Sensor Noise",
    subtitle="Gaussian Observation Noise Setting",
    border_color=(0, 255, 120),
    recurrent=False
)


# =====================================================
# VIDEO 3: PPO EXTREME OCCLUSION
# =====================================================

env = make_video_env(
    vehicle_occlusion=True,
    occlusion_prob=0.95,
    vehicles_count=28,
    duration=80,
    seed=303
)

record_video(
    model=ppo_extreme,
    env=env,
    path="videos/03_PPO_Extreme_Occlusion.mp4",
    title="PPO under Extreme Occlusion",
    subtitle="95% Vehicle Observation Occlusion",
    border_color=(255, 180, 0),
    recurrent=False
)


# =====================================================
# VIDEO 4: RECURRENT PPO EXTREME OCCLUSION
# =====================================================

env = make_video_env(
    vehicle_occlusion=True,
    occlusion_prob=0.95,
    vehicles_count=30,
    duration=80,
    seed=404
)

record_video(
    model=recurrent_extreme,
    env=env,
    path="videos/04_Recurrent_PPO_Extreme_Occlusion.mp4",
    title="Recurrent PPO / LSTM",
    subtitle="Memory-Based Policy under Extreme Occlusion",
    border_color=(255, 80, 80),
    recurrent=True
)


print("All enhanced videos generated successfully.")
print("Check the videos folder.")