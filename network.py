import networkx as nx
from core.entities import Agent, Connection

class Network():
    """

    """
    
    def __init__(self) -> None:
        self.id_agent = {}
        self.id_connections = {}
        self.agent_id_to_node_id = {}
        self.connection_id_to_edge_id = {}
        self.graph = nx.Graph()
    
    def add_agent(self, agent):
        self.id_agent.update({agent.get_id(): agent})

    def get_agent(self, id):
        return self.id_agent.get(id)
    
    def get_agents(self):
        """
        Returns all Agent in a
        """
        return self.id_agent.values()

    def get_agent_ids(self):
        return self.id_agent.keys()

    def connect(self, agent_a, agent_b):
        connection = Connection([agent_a, agent_b])
        connection.environment.setdefault("nodes",{}).setdefault("a", agent_a)
        #TODO: Link edges to connections
        connection.environment.setdefault("nodes",{}).setdefault("b", agent_b)
        self.add_connection(connection)
        return connection

    def add_connection(self, connection):
        self.id_connections.update({connection.get_id(): connection})

    def get_connection(self, id):
        return self.id_agent.get(id)

    def get_connections(self):
        return self.id_connections.values()
    
    def get_connection_ids(self):
        return self.id_agent.keys()
        
    def update(self, time_step):
        for connection in self.connections.values():
            connection.update(time_step)

        for agent in self.agents.values():
            agent.update(time_step)
