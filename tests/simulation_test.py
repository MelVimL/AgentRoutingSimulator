import pytest

from examples.qrouting import QRoutingAgent
from ars.behavior.connections import SimpleWireless
from ars.simulation import SimpleSimulation
from ars.factories import ConnectionFactory, AgentFactory


def test_simple_config(config: dict, sim: SimpleSimulation):
    net = sim.get_network()
    entities = sim.get_entity_scheduler().get_all()
    params_set = [x.config.get("test_param", False) for x in entities]
    assert all(params_set) and net.config.get("net_test_param")


def test_simple_q_simulation(config, sim: SimpleSimulation):
    net = sim.get_network()
    a_conf = config.get("Agent")
    c_conf = config.get("Connection")
    a_func = AgentFactory.create_mono_behavior(QRoutingAgent, a_conf)
    c_func = ConnectionFactory.create_mono_behavior(SimpleWireless, c_conf)
    net.generate_graph(net.graph, a_func, c_func)
    for i in range(20):
        sim.update()

    # net.debug_plt()

    assert True
