from neo4j import GraphDatabase
from app.core.config import settings
import logging

class GraphDB:
    def __init__(self):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            logging.info("Neo4j Driver Initialized Successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Neo4j driver: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def get_session(self):
        if not self.driver:
            raise ConnectionError("Neo4j driver not initialized")
        return self.driver.session()

    def verify_connectivity(self):
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            logging.error(f"Neo4j Connectivity Check Failed: {e}")
            return False

# Global Singleton Instance
graph_db = GraphDB()