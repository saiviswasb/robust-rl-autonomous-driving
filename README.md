# Improving Robustness of Reinforcement Learning for Autonomous Driving Under Sensor Noise and Partial Observability

This repository contains the final project for the Graduate Reinforcement Learning course.  
The project studies the robustness of reinforcement learning agents for autonomous driving using the `highway-env` simulator.

We evaluate PPO and Recurrent PPO under clean driving, Gaussian observation noise, vehicle occlusion, extreme occlusion, and long-training validation.

## Project Page

Project page:  
http://127.0.0.1:5500/index.html#videos

Colab notebook:  
https://colab.research.google.com/drive/1gJr58KqC9kCuX36MabSd4KsunIXRJ5RW?usp=sharing

GitHub repository:  
https://github.com/saiviswasb/robust-rl-autonomous-driving/

---

## Team Members

- Sai Viswas
- Nadini
- Kanika

Institution: National Yang Ming Chiao Tung University

---

## Project Motivation

Autonomous driving systems must remain reliable when sensor observations are noisy, incomplete, or partially unavailable. In real-world driving, cameras, LiDAR, radar, or perception modules may produce imperfect information due to weather, occlusion, latency, or sensor noise.

This project investigates how reinforcement learning policies behave under these conditions. The main goal is to evaluate whether standard PPO and memory-based Recurrent PPO can maintain safe and stable driving behavior under observation corruption.

---

## Research Questions

1. How robust is PPO under Gaussian sensor noise?
2. How does vehicle occlusion affect autonomous driving performance?
3. Can Recurrent PPO with LSTM memory improve robustness under partial observability?
4. Does PPO remain stable under longer training validation?

---

## Methodology

The project uses the `highway-env` autonomous driving simulator. We modify the observation stream using custom wrappers:

- Gaussian noise wrapper
- Vehicle occlusion wrapper
- Eco-driving reward shaping wrapper
- Extreme occlusion setting

The evaluated algorithms are:

- PPO
- Recurrent PPO with LSTM

Evaluation metrics:

- Mean reward
- Standard deviation of reward
- Collision rate
- Average speed

---

## Main Pipeline

<img width="1000" height="715" alt="pipeline_diagram" src="https://github.com/user-attachments/assets/d4e7a11b-8323-4c59-807b-1dc125a046e6" />


The experimental pipeline includes environment simulation, observation corruption, PPO/Recurrent PPO training, policy actions, and evaluation using reward, collision rate, and speed.

---

## Environment

<img width="1918" height="522" alt="highway_env" src="https://github.com/user-attachments/assets/eaaa5a21-f6bf-4df7-ba9a-7a44d52bc35a" />


The environment is based on `highway-env`, where the agent learns lane-changing and driving behavior in traffic.

---

## Final Results

| Experiment | Mean Reward | Std Reward | Collision Rate | Average Speed |
|-----------|------------:|-----------:|---------------:|--------------:|
| PPO Clean 10k | 12.749 | 3.028 | 0.10 | 19.988 |
| PPO Gaussian Noise 10k | 13.842 | 0.419 | 0.00 | 20.038 |
| PPO Eco + Noise 10k | 14.109 | 0.400 | 0.00 | 20.038 |
| PPO Strong Noise 10k | 14.065 | 0.495 | 0.00 | 20.038 |
| PPO Extreme Occlusion 20k | 14.065 | 0.514 | 0.00 | 20.038 |
| Recurrent PPO Extreme 20k | 12.360 | 3.878 | 0.70 | 23.706 |
| PPO Extreme Occlusion 100k | 13.999 | 1.603 | 0.05 | 20.154 |

---

## Main Result Graphs

### Reward Comparison

<img width="1189" height="490" alt="reward_comparison" src="https://github.com/user-attachments/assets/740a28f7-dd5b-4d00-bd00-9d5b85dd6db0" />


### Collision Rate Comparison

<img width="1189" height="490" alt="collision_comparison" src="https://github.com/user-attachments/assets/f46d4fda-427a-4fbc-bff6-73ba6101affa" />


---

## Noise Sensitivity Study

The noise sensitivity experiment evaluates PPO under increasing Gaussian observation noise levels.

### Reward vs Noise

<img width="790" height="490" alt="noise_reward" src="https://github.com/user-attachments/assets/8896aa41-7cae-42e3-8445-f27e8753ba8e" />


### Collision Rate vs Noise

<img width="790" height="490" alt="noise_collision" src="https://github.com/user-attachments/assets/83f8cf9a-0205-477e-9978-3ef221a9e94e" />


Key observation: PPO remained stable across Gaussian noise levels, indicating that additive noise alone did not significantly degrade performance.

---

## Occlusion Sensitivity Study

The occlusion sensitivity experiment evaluates PPO under increasing vehicle observation occlusion.

### Reward vs Occlusion

<img width="790" height="490" alt="occlusion_reward" src="https://github.com/user-attachments/assets/fcd52fe6-da4a-45ac-919d-104c0ade6b9c" />


### Collision Rate vs Occlusion

<img width="790" height="490" alt="occlusion_collision" src="https://github.com/user-attachments/assets/4295e8e6-3d80-4b62-833a-c3ba274e643b" />

Key observation: vehicle occlusion was more challenging than Gaussian noise because it removes important information from the observation space.

---

## Behavioral Videos

The project page includes rollout videos for:

- PPO clean driving
- PPO under Gaussian noise
- PPO under extreme occlusion
- Recurrent PPO under extreme occlusion

Videos are available in:

```text
docs/videos/
