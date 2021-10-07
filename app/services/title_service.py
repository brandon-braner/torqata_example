from py2neo import Graph

from app.providers.db import neo_graph
from app.schemas.title_schemas import TitleResponseSchema


class TitleService:

    def __init__(self):
        self.graphdb: Graph = neo_graph()
        self.node_type = "Title"

    def get_movies(self, skip: int = 0, limit: int = 10, order_field: str = "title",
                   order_direction: str = "ASC"):
        """Get list of movies."""
        order_by = f"_.{order_field} {order_direction}"
        movies = self.graphdb.nodes.match(self.node_type, title_type="Movie").limit(limit).order_by(order_by)
        if skip > 0:
            movies.skip(skip)
        result = movies.all()
        return result
