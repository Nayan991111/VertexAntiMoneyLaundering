import logging
from neo4j import GraphDatabase
from app.core.config import settings

# Configure Logging
logger = logging.getLogger(__name__)

class GraphService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphService, cls).__new__(cls)
            # Initialize the driver once
            try:
                cls._instance.driver = GraphDatabase.driver(
                    settings.NEO4J_URI, 
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                logger.info("✅ Neo4j Driver Initialized.")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Neo4j Driver: {e}")
                cls._instance.driver = None
        return cls._instance

    def close(self):
        if self.driver:
            self.driver.close()

    def check_connection(self):
        """Verifies connectivity to the Graph Database."""
        if not self.driver:
            return False
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                return result.single()[0] == 1
        except Exception as e:
            logger.error(f"Neo4j Connection Check Failed: {e}")
            return False

    def ingest_transaction(self, sender_id: str, receiver_id: str, amount: float, txn_id: str):
        """
        Creates nodes (Person) and relationship (SENT_FUNDS).
        Merge ensures we don't create duplicate people.
        """
        if not self.driver: 
            return
            
        query = """
        MERGE (a:Person {id: $sender_id})
        MERGE (b:Person {id: $receiver_id})
        MERGE (a)-[r:SENT_FUNDS]->(b)
        SET r.amount = $amount, r.txn_id = $txn_id, r.timestamp = datetime()
        """
        try:
            with self.driver.session() as session:
                session.run(query, sender_id=sender_id, receiver_id=receiver_id, amount=amount, txn_id=txn_id)
        except Exception as e:
            logger.error(f"Failed to ingest transaction to graph: {e}")

    def detect_circular_flow(self):
        """
        Detects cycles: A -> B -> C -> A (The 'Ring').
        Limit 10 to prevent data overload.
        """
        if not self.driver: 
            return []

        query = """
        MATCH path = (n:Person)-[:SENT_FUNDS*2..4]->(n)
        RETURN [node in nodes(path) | node.id] as path_ids,
               [rel in relationships(path) | rel.amount] as amounts,
               length(path) as hops
        LIMIT 10
        """
        try:
            with self.driver.session() as session:
                result = session.run(query)
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Graph Query Failed: {e}")
            return []

    def clear_graph(self):
        """Wipes the database for testing"""
        if not self.driver: return
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

# Export Singleton
graph_service = GraphService()