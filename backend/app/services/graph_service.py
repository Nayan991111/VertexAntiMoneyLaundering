from app.db.graph import graph_db

class GraphService:
    def create_customer_node(self, customer_id: int, name: str, risk_score: float):
        """
        Idempotent creation of a Customer Node in the graph.
        """
        query = """
        MERGE (c:Customer {id: $id})
        ON CREATE SET c.name = $name, c.risk_score = $risk_score, c.created_at = datetime()
        ON MATCH SET c.risk_score = $risk_score
        RETURN c
        """
        with graph_db.get_session() as session:
            session.run(query, id=customer_id, name=name, risk_score=risk_score)

    def record_transaction(self, sender_id: int, counterparty_account: str, amount: float, currency: str):
        """
        Projects a transaction as a directional relationship.
        (Customer)-[:SENT_MONEY {amount: 500}]->(Account)
        """
        query = """
        MATCH (c:Customer {id: $sender_id})
        MERGE (a:ExternalAccount {account_number: $counterparty_account})
        MERGE (c)-[r:TRANSFERRED {amount: $amount, currency: $currency, timestamp: datetime()}]->(a)
        RETURN type(r)
        """
        with graph_db.get_session() as session:
            session.run(query, 
                        sender_id=sender_id, 
                        counterparty_account=counterparty_account, 
                        amount=amount, 
                        currency=currency)

graph_service = GraphService()
                  