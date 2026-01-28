from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ZeTheta Compliance Engine"
    API_V1_STR: str = "/api/v1"
    
    # Postgres (Transactional)
    DATABASE_URL: str = "postgresql+asyncpg://admin:secure_password_123@localhost:5432/compliance_db"
    
    # Neo4j (Graph - AML)
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "secure_graph_pass_123"

    class Config:
        env_file = ".env"

settings = Settings()