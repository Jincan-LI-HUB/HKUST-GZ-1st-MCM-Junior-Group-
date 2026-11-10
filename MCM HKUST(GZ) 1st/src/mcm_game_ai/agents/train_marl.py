# agents/train_marl.py
from config import *
import torch
# ...
import torch
import torch.optim as optim
from torch.distributions import Categorical
from core.game import GameEnv
from agents.policy_net import SimplePolicy
import numpy as np

alice_policy = SimplePolicy()
bob_policy = SimplePolicy()
alice_opt = optim.Adam(alice_policy.parameters(), lr=3e-4)
bob_opt = optim.Adam(bob_policy.parameters(), lr=3e-4)

def select_action(policy, state, legal_moves):
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    logits = policy(state_tensor)
    mask = torch.tensor([0 if (i+1) in legal_moves else -1e9 for i in range(100)], dtype=torch.float32)
    logits += mask
    dist = Categorical(logits=logits)
    action_idx = dist.sample()
    return action_idx.item() + 1, dist.log_prob(action_idx)

for episode in range(5000):
    env = GameEnv()
    log_probs_a, log_probs_b = [], []
    rewards_a, rewards_b = [], []

    while not env.done:
        state = env.get_state_vec()
        legal = env.get_legal_moves()

        if env.player == 0:  # Alice
            action, lp = select_action(alice_policy, state, legal)
            log_probs_a.append(lp)
        else:  # Bob
            action, lp = select_action(bob_policy, state, legal)
            log_probs_b.append(lp)

        env = env.make_move(action)
        if env is None: break

    sa, sb, winner = env.get_result()
    total_reward_a = sa + (100 if sa > sb else 0)
    total_reward_b = sb + (100 if sb >= sa else 0)

    loss_a = -sum(log_probs_a) * total_reward_a
    loss_b = -sum(log_probs_b) * total_reward_b

    alice_opt.zero_grad(); loss_a.backward(); alice_opt.step()
    bob_opt.zero_grad(); loss_b.backward(); bob_opt.step()

    if episode % 500 == 0:
        print(f"Episode {episode} | Alice: {sa}, Bob: {sb} | Winner: {winner}")

torch.save(alice_policy.state_dict(), "../data_output/alice_policy.pth")
torch.save(bob_policy.state_dict(), "../data_output/bob_policy.pth")