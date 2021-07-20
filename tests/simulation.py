from core import Simulation, Agent, Connection

def test_simple_simulation():

    sim = Simulation()
    sim.add_behavior(Agent, )
    sim.add_behavior(Connection,)
    sim.remove_behavior()
    sim.add_graph()
    
    sim.load()
    sim.store()
    
    for i in range(2000):
        sim.update(i)
    

    