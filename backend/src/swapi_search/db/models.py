from sqlalchemy import Column, Integer, String, Text, JSON, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SwapiResource(Base):
    """
    Represents a normalized resource from SWAPI, stored in a unified table.
    This design simplifies search queries by avoiding complex joins.
    """
    __tablename__ = "swapi_resource"

    id = Column(Integer, primary_key=True, index=True)
    swapi_id = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)
    searchable_text = Column(Text, nullable=False)
    
    data = Column(JSON, nullable=False)
    
    searchable_text = Column(Text, nullable=False)

    __table_args__ = (
        Index(
            "ix_swapi_resource_searchable_text_gin",
            searchable_text,
            postgresql_using="gin",
            postgresql_ops={"searchable_text": "gin_trgm_ops"},
        ),
    )