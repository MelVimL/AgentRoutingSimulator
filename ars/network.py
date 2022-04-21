from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .core.entities import Connection, Agent
from .utils.spatial import Position
from functools import cache
import networkx as nx
from .utils.datastructures import SpaceStorage, KDTree


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

    def get_agents(self) -> list[Agent]:
        return list(self.graph)

    @cache
    def get_agent_by_name(self, name):
        for agent in self.get_agents():
            if str(agent) == name:
                return agent

    def connect(self,
                agent_a: Agent,
                agent_b: Agent,
                connection: Connection) -> None:
        self._bind_agents_to_connection(agent_a, agent_b, connection)
        self.graph.add_edge(agent_a, agent_b, connection=connection)

    def _bind_agents_to_connection(self,
                                   agent_a: Agent,
                                   agent_b: Agent,
                                   connection: Connection) -> None:
        agent_a.set_network(self)
        agent_b.set_network(self)

        connection.set_network(self)
        connection.set_agent(agent_a)
        connection.set_agent(agent_b)

    def get_all_connections(self) -> list[Connection]:
        return [x[2] for x in self.graph.edges.data("connection", None)]

    def get_connections(self, agent) -> list[Connection]:
        result = []
        graph = self.graph

        for other_agent in graph.neighbors(agent):
            connection = self.get_connection(agent, other_agent)
            result.append(connection)

        return result

    def get_connection(self, a: Agent, b: Agent) -> Connection:
        return self.graph.get_edge_data(a, b)["connection"]

    def get_graph(self) -> nx.Graph:
        return self.graph

    def set_graph(self, graph) -> None:
        self.graph = graph

    def generate_graph(self,
                       graph_scheme: nx.Graph,
                       a_gen_func,
                       c_gen_func):
        self.set_graph(nx.empty_graph())
        positions = nx.spring_layout(graph_scheme)
        id_agent_map = {}
        for node in graph_scheme.nodes:
            x, y = positions.get(node)
            id_agent_map.update({node: a_gen_func(Position(x, y))})

        for edge in graph_scheme.edges:
            a_key, b_key = edge
            a = id_agent_map.get(a_key)
            b = id_agent_map.get(b_key)
            c = c_gen_func()
            self.connect(a, b, c)

    def get_space(self) -> SpaceStorage:
        return self.space

    def get_neighbors(self, agent) -> list:
        return [x for x in self.graph.neighbors(agent)]

    def debug_plt(self) -> None:
        import networkx as nx
        import matplotlib.pyplot as plt

        pos = {x: x.get_position().to_tuple() for x in self.graph.nodes}
        nx.draw(self.graph, pos, with_labels=True,
                connectionstyle='arc3, rad = 0.1')

        plt.show()

    def __len__(self):
        return len(self.get_agents())
