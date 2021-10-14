import networkx as nx

class Network():
    """

    """
    
    def __init__(self) -> None:
        self.graph: nx.Graph = nx.Graph()
    
    def add_agent(self, agent):
        self.graph.add_node(agent)

    def get_agents(self):
        """
        Returns all Agent in a
        """
        return self.graph.nodes

    def connect(self, agent_a, agent_b, connection):
        self.graph.add_edge(agent_a, agent_b, connection=connection)

    def get_connections(self):
        return [x[2] for x in self.graph.edges.data("connection", None)]
    
    def get_connection_ids(self):
        return self.id_agent.keys()
        
    def update(self, time_step):
        for connection in self.connections.values():
            connection.update(time_step)

        for agent in self.agents.values():
            agent.update(time_step)