
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.entities import Connection, Agent


import networkx as nx
from utils.datastructures import SpaceStorage, KDTree


class Network():
    """

    """

    def __init__(self, config={}) -> None:
        self.config: dict = config
        self.graph: nx.Graph = nx.Graph()
        self.space: SpaceStorage = KDTree()

    def add_agent(self, agent):
        self.graph.add_node(agent)
        self.space.put(agent)

    def get_agents(self)-> list[Agent]:
        return self.graph.nodes

    def connect(self, agent_a: Agent, agent_b: Agent, connection: Connection) -> None:
        agent_a.set_network(self)
        agent_b.set_network(self)

        connection.set_network(self)
        connection.set_agent(agent_a)
        connection.set_agent(agent_b)

        self.graph.add_edge(agent_a, agent_b, connection=connection)

    def get_all_connections(self) -> list[Connection]:
        return [x[2] for x in self.graph.edges.data("connection", None)]

    def get_connections(self, agent) -> list[Connection]:
        return [self.graph.get_edge_data(agent, x)["connection"] for x in self.graph.neighbors(agent)]

    def get_graph(self) -> nx.Graph:
        return self.graph

    def get_space(self) -> SpaceStorage:
        return self.space

    def debug_plt(self) -> None:
        import networkx as nx
        import matplotlib.pyplot as plt

        #pos = nx.spring_layout(self.graph)
        pos = {x: x.get_position().to_tuple() for x in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=True,
                connectionstyle='arc3, rad = 0.1')
        edge_labels = dict([((u, v,), d['connection'])
                           for u, v, d in self.graph.edges(data=True)])

        plt.show()
