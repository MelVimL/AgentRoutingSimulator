from core.entities import Agent, Connection

class ConnectionFactory:
    

    @staticmethod
    def create_wireless_connection():
        connection = Connection()
        connection.add_behavior()
        connection.add_behavior()
        return connection



class AgentFactory:
    pass
