# web/app.py
import gradio as gr
import torch
from core.game import GameEnv
from agents.policy_net import SimplePolicy
from explain.strategy_explainer import explain_strategy

alice_policy = SimplePolicy()
alice_policy.load_state_dict(torch.load("../data_output/alice_policy.pth"))
alice_policy.eval()

def play_and_explain(chain_str):
    try:
        chain = list(map(int, chain_str.split()))
        env = GameEnv()
        env.chain = chain
        env.scores = [sum(chain[i] for i in range(0,len(chain),2)), 
                      sum(chain[i] for i in range(1,len(chain),2))]
        env.player = len(chain) % 2  # 0=Alice, 1=Bob

        explanation = explain_strategy(alice_policy, env)
        return explanation
    except Exception as e:
        return f"输入错误: {e}"

iface = gr.Interface(
    fn=play_and_explain,
    inputs="text",
    outputs="text",
    title="🎮 整除链博弈 AI 策略解释器",
    description="输入当前数字链（空格分隔），AI 将告诉你它的思考过程。",
    examples=[["60 30 15"], ["2 4 8 16"], ["97"]]
)
iface.launch()