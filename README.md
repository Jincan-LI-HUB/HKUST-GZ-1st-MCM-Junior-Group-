# Game on Integers: Graph Optimization and Adversarial Learning

**2025 HKUST (Guangzhou) 1st Mathematical Contest in Modeling — Junior Group**  
**Team:** Monte Carlo Gamblers  
**Topic:** Divisibility-chain optimization and competitive strategy  
**Tools:** Python · Graph Algorithms · Ant Colony Optimization · Depth-First Search · PyTorch

> A mathematical modeling project investigating how graph structure, combinatorial optimization, and learning-based agents can solve a two-player integer-selection game.

**Project documents:** [Competition problem](MCM%20HKUST%28GZ%29%201st/2025%20MCM%20Junior%20Group%20Problem%20Game%20on%20Integers.pdf) · [Team report](MCM%20HKUST%28GZ%29%201st/Monte_Carlo_Gamblers_Junior_Group.pdf)

## Overview

The *Game on Integers* asks Alice and Bob to construct a sequence of distinct integers from **1 through 100**. Alice moves first, and the players alternate. Each subsequent integer must either divide the previous integer or be divisible by it. A player's payoff is the sum of the integers chosen on their turns; the game ends when no legal move remains.

We investigated two related questions:

1. **Cooperative optimization:** How large can the total sum of a valid chain be when both players cooperate?
2. **Competitive strategy:** How can Alice use the game's divisibility structure to gain an advantage over Bob?

We modeled the rules as a **weighted, undirected divisibility graph** and developed different approaches for the cooperative and competitive settings. The submitted report combines ant colony optimization (ACO), an initial depth-first search (DFS) baseline, mathematical opening-strategy analysis, and a proposed multi-agent adversarial reinforcement-learning framework.

## Mathematical Formulation

Let the graph contain one vertex for each integer in `{1, 2, ..., 100}`. Connect distinct vertices `i` and `j` when `i` divides `j` or `j` divides `i`.

A legal sequence is a **simple path** through this graph: adjacent numbers satisfy the divisibility rule, and vertices cannot be repeated. Each vertex has weight equal to its integer value.

- **Cooperative objective:** Maximize `sum(chain)` over legal paths.
- **Competitive objective:** Alice maximizes the sum of values at odd-numbered positions while Bob maximizes the sum at even-numbered positions, under alternating legal play.

This formulation converts the original game into a combination of **weighted path search** and **sequential, adversarial decision-making**.

## Methods

### 1. Depth-First Search with Pruning (baseline)

The initial approach explores legal paths using DFS. To reduce the search space, it prioritizes large integers, considers connectivity to larger neighbors, and prunes branches whose remaining possible value cannot improve the best sum found so far.

This provides a useful search baseline, but it is **time-limited** and does not establish a global optimum.

**Source:** [`src/ACO alg/DFS+pruning.py`](MCM%20HKUST%28GZ%29%201st/src/ACO%20alg/DFS%2Bpruning.py)

### 2. Ant Colony Optimization (cooperative scenario)

The main cooperative algorithm constructs chains using artificial ants that traverse the divisibility graph without revisiting vertices. The move preference combines:

- **Pheromone intensity:** Reinforcement of edges observed in high-scoring paths.
- **A value-based heuristic:** Preference for visiting larger candidate integers.
- **Pheromone evaporation:** A mechanism for balancing exploitation and continued exploration.

The code evaluates each candidate chain by its total integer sum, retains the best valid chain, and reports its length, unused integers, and alternating-player score split.

**Default parameters in the committed implementation:**

| Parameter | Value |
| --- | ---: |
| Integer range | 1–100 |
| Ants per iteration | 200 |
| Maximum iterations | 1,000 |
| Pheromone importance (`alpha`) | 1 |
| Heuristic importance (`beta`) | 2 |
| Evaporation rate | 0.3 |
| Time limit | 300 seconds |

**Source:** [`src/ACO alg/ACO_final_parameter.py`](MCM%20HKUST%28GZ%29%201st/src/ACO%20alg/ACO_final_parameter.py)

### 3. Opening-Strategy Analysis (competitive scenario)

The report studies how Alice can exploit the graph's structure, particularly by opening with **large semiprimes** (such as `91`) to limit Bob's immediate responses. It also discusses how small, highly connected numbers can serve as bridges between different divisibility branches.

The resulting strategic idea is to evaluate a move not only by its immediate score, but also by its effect on the opponent's future options and the remaining path.

These recommendations are **heuristic insights**, not a proof of optimal play.

### 4. Multi-Agent Learning and Experimental Extensions

The `mcm_game_ai` directory contains an experimental AI implementation:

- A **game environment** that enforces alternating turns, legal moves, and score tracking.
- Two **PyTorch policy networks** (one per player) operating on a 102-dimensional state: 100 used-number indicators, normalized last number, and current player.
- **Action masking** to disallow invalid choices, with a policy-gradient-style self-play training script.
- Separate **graph neural network (GNN)**, **Monte Carlo Tree Search (MCTS)**, strategy explanation, and **Gradio interface** prototypes.

The report describes a broader *Multi-Agent Adversarial Reinforcement Learning* (MAARF) framework. **The committed training script is a simplified experimental implementation and does not reproduce every reward-shaping or exploration component described in the paper.** The GNN/MCTS and UI prototypes also rely on model checkpoints or setup steps not included in this repository.

**Source directory:** [`src/mcm_game_ai/`](MCM%20HKUST%28GZ%29%201st/src/mcm_game_ai/)

## Results Reported in the Submission

The following figures are taken from the [team report](MCM%20HKUST%28GZ%29%201st/Monte_Carlo_Gamblers_Junior_Group.pdf). They are **reported experimental outcomes**, not results independently reproduced from a fresh run of the public repository.

| Scenario | Metric | Reported value |
| --- | --- | ---: |
| Cooperative (ACO) | Best valid-chain sum | **3,551** |
| Cooperative (ACO) | Mean best sum across reported runs | 3,550.2 |
| Cooperative (ACO) | Mean best-chain length | 77 integers |
| Competitive (MAARF evaluation) | Alice win rate | **78.6%** |
| Competitive (MAARF evaluation) | Alice mean score | 942.3 |
| Competitive (MAARF evaluation) | Bob mean score | 876.1 |
| Competitive (MAARF evaluation) | Mean chain length | 38.2 integers |

The central modeling insight is that **graph connectivity matters alongside numerical value**. High-scoring cooperative solutions need both valuable integers and routes that keep the chain extendable; in competition, controlling the opponent's next legal choices may matter more than maximizing the immediate gain.

## Repository Structure

| Path | Contents |
| --- | --- |
| [`MCM HKUST(GZ) 1st/2025 MCM Junior Group Problem Game on Integers.pdf`](MCM%20HKUST%28GZ%29%201st/2025%20MCM%20Junior%20Group%20Problem%20Game%20on%20Integers.pdf) | Original competition problem statement |
| [`MCM HKUST(GZ) 1st/Monte_Carlo_Gamblers_Junior_Group.pdf`](MCM%20HKUST%28GZ%29%201st/Monte_Carlo_Gamblers_Junior_Group.pdf) | Submitted mathematical modeling report |
| [`src/ACO alg/ACO_final_parameter.py`](MCM%20HKUST%28GZ%29%201st/src/ACO%20alg/ACO_final_parameter.py) | Ant colony optimization for high-sum chains |
| [`src/ACO alg/DFS+pruning.py`](MCM%20HKUST%28GZ%29%201st/src/ACO%20alg/DFS%2Bpruning.py) | DFS search with heuristic ordering and pruning |
| [`src/mcm_game_ai/core/game.py`](MCM%20HKUST%28GZ%29%201st/src/mcm_game_ai/core/game.py) | Rules and state of the competitive game |
| [`src/mcm_game_ai/agents/`](MCM%20HKUST%28GZ%29%201st/src/mcm_game_ai/agents/) | Policy network and self-play training prototype |
| [`src/mcm_game_ai/core/`](MCM%20HKUST%28GZ%29%201st/src/mcm_game_ai/core/) | GNN and MCTS experimental modules |
| [`src/mcm_game_ai/explain/`](MCM%20HKUST%28GZ%29%201st/src/mcm_game_ai/explain/) | Policy-output explanation helper |
| [`src/mcm_game_ai/web/`](MCM%20HKUST%28GZ%29%201st/src/mcm_game_ai/web/) | Gradio interface prototype |

*All `src/` paths in this table are relative to `MCM HKUST(GZ) 1st/`.*

## Getting Started

### Requirements

- **Python 3.x**
- **No external Python packages** for the standalone DFS and ACO scripts (they use the standard library).
- For the experimental AI modules, additional dependencies include **PyTorch**, **NumPy**, **PyTorch Geometric**, and **Gradio**. These are not pinned in a dependency manifest.

### Clone the repository

```bash
git clone https://github.com/Jincan-LI-HUB/HKUST-GZ-1st-MCM-Junior-Group-.git
cd 'HKUST-GZ-1st-MCM-Junior-Group-/MCM HKUST(GZ) 1st'
```

### Run the ant colony optimization script

```bash
python 'src/ACO alg/ACO_final_parameter.py'
```

The script searches for valid high-sum paths under its built-in time limit and prints the best chain and its summary statistics. Because the search is randomized and does not set a fixed random seed, results may vary between runs.

### Run the DFS baseline

```bash
python 'src/ACO alg/DFS+pruning.py'
```

The DFS script runs a time-limited search and prints the best chain found. Neither script is an exact solver with a global-optimality certificate.

### Exploring the AI prototypes

The code under `src/mcm_game_ai/` is provided primarily for inspection and further development. A fully reproducible end-to-end training, evaluation, and deployment workflow is **not included**; in particular, pretrained network weights and a verified dependency environment are absent. The game environment and model definitions can nevertheless be studied independently.

## Reproducibility and Limitations

- **Heuristic versus exact solutions:** The ACO and time-limited DFS methods seek strong valid chains but do not prove optimality.
- **Reported versus reproducible metrics:** The numerical results above come from the submitted paper; associated evaluation logs, complete trained checkpoints, and an automated reproduction script are not provided.
- **Paper/code differences:** The report's full MAARF description includes methodological details not implemented in the checked-in `train_marl.py` prototype. Interpret the competitive results as *report-level findings*, not as performance guaranteed by this particular script.
- **Evaluation reporting:** The report's detailed competitive results table states a 78.6% win rate, while an earlier section mentions 71%; this discrepancy should be reconciled before treating the figure as a definitive benchmark.
- **Scope:** The model and experiments concern integers 1–100. Generalization to larger integer ranges or stronger adversaries has not been established here.

## Team and Acknowledgments

**Monte Carlo Gamblers** — Jincan Li, Wenlue Chai, Zheng Tian, and Zixian Guo.  
Developed for the **2025 HKUST (Guangzhou) 1st Mathematical Contest in Modeling, Junior Group**.

The original problem statement and research references are included in the competition materials and [team report](MCM%20HKUST%28GZ%29%201st/Monte_Carlo_Gamblers_Junior_Group.pdf).

---

*This repository is an academic competition archive and a record of the team's mathematical modeling and computational experiments.*
