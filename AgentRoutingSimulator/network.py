import networkx as nx
from utils.datastructures import SpaceStorage, KDTree 


class Network():
    """

    """
    
    def __init__(self) -> None:
        self.graph: nx.Graph = nx.Graph()
        self.space: SpaceStorage = KDTree()
    
    def add_agent(self, agent):
        self.graph.add_node(agent)
        self.space.put(agent)

    def get_agents(self):
        """
        Returns all Agent in a
        """
        return self.graph.nodes

    def connect(self, agent_a, agent_b, connection):
        agent_a.set_network(self)
        agent_b.set_network(self)
    
        connection.set_network(self)
        
        self.graph.add_edge(agent_a, agent_b, connection=connection)

    def get_all_connections(self):
        return [x[2] for x in self.graph.edges.data("connection", None)]
    
    def get_connections(self, agent):
        return [self.graph.get_edge_data(agent, x)["connection"] for x in self.graph.neighbors(agent)]    

    def get_connection_ids(self):
        return self.id_agent.keys()
        
    def update(self, time_step):
        for connection in self.connections.values():
            connection.update(time_step)

        for agent in self.agents.values():
            agent.update(time_step)
    
    def debug_plt(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        #pos = nx.spring_layout(self.graph)
        pos = {x: x.get_position().to_tuple()  for  x in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
        edge_labels=dict([((u,v,),d['connection']) for u,v,d in self.graph.edges(data=True)])

        plt.show()