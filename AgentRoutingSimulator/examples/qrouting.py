from queue import Queue
from behavior.agents import AgentBehavior


class QRoutingAgent(AgentBehavior):

    def __init__(self, config) -> None:
        self.alpha = config.get("alpha", 0.)
        self.beta = config.get("beta", 0.5)
        self.delta = config.get("delta", 1.)
        self.default_q = config.get("default_q", 0.)
        self.agent = self.get_agent()
        self.net = self.agent.get_network()
        self.cons = self.net.get_connections(self.agent)
        self._q_table = {}
        self._t_table = {}
        super().__init__()

    def update(self, time_step: int) -> None:

        if  self.get_has_messages():
            message = self.get_message()
            destination = message.get_destination()
            neigbors = self.get_neigbors()
            next_hop = self.select_best_choice(neigbors, destination)

            q = self.message 
            s = self.send(message, next_hop)
            t = self.neigbor_estimation(destination, next_hop)
            old_q_value = self.quality_func(destination, next_hop)
            new_q_value = old_q_value + self.alpha * \
                ((s + q + t) - old_q_value)
            self._q_table.get(destination).update({next_hop: new_q_value})

        return super().update(time_step)

    def quality_func(self, destination, next_hop):
        return self._q_table.setdefault(destination, {}).setdefault(next_hop, self.default_q)

    def neigbor_estimation(self, destination, neigbors, beta, delta):
        min(neigbors, key=lambda x: x.T(destination, neigbors, beta, delta))
    def select_min(self, neigbors, destination):
        return min(neigbors, lambda x: self.Q(destination, x))

    def select_best_choice(self, neigbors, destination):
        return self.select_min(neigbors, destination)

    def get_neigbors(self):
        agent = self.get_agent()
        return agent.get_network().get_graph().neigbors(agent)
