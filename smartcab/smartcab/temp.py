from simulator import Simulator
from environment import Agent, Environment


env = Environment()
agent = env.create_agent(LearningAgent,learning=True)
env.set_primary_agent(agent, enforce_deadline=True)
sim = Simulator(env,update_delay=0.01,log_metrics=True,optimized=True)