import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.trialNumber = 1
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        for i in ['green', 'red']:  # possible lights
            for j in ['forward', 'left', 'right','None']:  ## possible next_waypoints
                for on in ['forward','left','right',None]:
                    state = (j,i,on)  
                    self.Q[state]={}
                    for k in ['forward', 'left', 'right','None']:  ## possible next_waypoints
                        self.Q[state][k] = 0.0

        # Set any additional class parameters as needed
        self.Qtable = {}  #empty Qtable to be filled during update
        self.lesson_counter = 0  #counts number of steps learned
        self.steps_counter = 0 #counts steps in the trial
        #self.Q_init = 0  #initial Q^ values for new state-actions not observed yet.
        self.Q_init = 13 #initial Q^ values for new state-actions not observed yet.

#        self.gamma = 0
#        self.gamma = 0.1  #discounting rate of future rewards

        """The output for the Logistic function for epsilon ranges from 0.75 to 0.99, and increases as the number of total
        steps increases during the learning process.  Random actions will give way to
        the 'best' action, gradually, but will never exceed 99%."""

#        self.alpha = 1 - ( 0.5 / (1 + math.exp(-0.05*(self.lesson_counter-100)))) #alpha ranges from 1 to 0.5
        self.possible_actions = ["forward","left","right","None"]
        
        self.reward_previous = None
        self.action_previous = None
        self.state_previous = None
        
    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        self.trialNumber = self.trialNumber+1
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # mychange
#        self.epsilon = 1
#        self.epsilon = self.epsilon -0.05
#        self.epsilon = 0.75 + (0.24 / (1+( math.exp(-0.1*(self.lesson_counter-40)))))        
#        self.epsilon = 1 - (1/(1+math.exp(-0.1*self.alpha*(self.trialNumber-40))))
        self.epsilon = self.epsilon -0.00025*self.trialNumber
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        if testing:
            self.alpha=0
            self.epsilon=0
        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        # When learning, check if the state is in the Q-table
        #   If it is not, create a dictionary in the Q-table for the current 'state'
        #   For each action, set the Q-value for the state-action pair to 0
        
#        state = None
        state = (waypoint,inputs['light'],inputs['oncoming'])
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        max_v = None
        
        if state in self.Q:
            _actions = self.Q[state]
            #index = actions.index(max(actions))
            #print("Q for current states = {} max = {}".format(_actions,max(_actions)))
            v = list(_actions.values())
            max_v = max(v)


        return max_v
#        return maxQ


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0

        if self.learning:
            if state in self.Q:
                pass
            else:
                self.Q[state]['forward'] =   0.0
                self.Q[state]['left']    =   0.0
                self.Q[state]['right']   =   0.0
                self.Q[state]['None']   =   0.0
                
        
        return

       
    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()
        action = None

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state
        
        if self.learning:
            p = random.uniform(0,1)
            if p< self.epsilon:
                action = random.choice(self.possible_actions)
            else:
                max_v=self.get_maxQ(state)
                if max_v:
                    actions=self.Q[state].keys()
                    max_actions=[action for action in actions if self.Q[state][action]==max_v]
                    action = random.choice(max_actions)
                else:
                    action = random.choice(self.possible_actions)
        else:
            action = random.choice(self.possible_actions)
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """
            

        next_waypoint = self.planner.next_waypoint()
        next_inputs = self.env.sense(self)
        
        #next_state = (next_inputs['light'],next_inputs['oncoming'], next_waypoint)
        next_state = (next_waypoint,next_inputs['light'],next_inputs['oncoming'])
            
        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        if self.learning:
            print("next state {}".format(self.Q[next_state]))
            _actions = self.Q[next_state]
            v = list(_actions.values())
            k = list(_actions.keys())
            maxFutureAction = k[v.index(max(v))]
            v1 = self.Q[next_state][maxFutureAction]
            print("learning from {} {} {}".format(state,action,v1))
#            gamma = 0.1;
#            new_value = self.Q[state][action] + self.alpha*(reward +gamma*v1-self.Q[state][action])
            self.Q[state][action] = self.Q[state][action] + self.alpha * (reward - self.Q[state][action])
        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        
        self.createQ(state)                 # Create 'state' in Q-table
        
        action = self.choose_action(state)  # Choose an action
        _action = action
        if action == 'None':
            _action = None
        reward = self.env.act(self, _action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent)
    agent.learning = True
    agent.alpha=0.6
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent)
    env.enforce_deadline = True
    
    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env,log_metrics=True, update_delay=0.01, optimized=True)

    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=20,tolerance=0.15)
#    print agent.Q

if __name__ == '__main__':
    run()
