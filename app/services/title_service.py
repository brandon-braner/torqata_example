from app.providers.db import neo_engine


class TitleService:

    def __init__(self):
        self.graphdb = neo_engine()
        self.node_type = "Title"

    def get_movies(self, skip: int = 0, limit: int = 10, order_field: str = "title",
                   order_direction: str = "ASC"):
        """Get list of movies."""
        order_by = f"m.{order_field} {order_direction}"
        with self.graphdb.session() as session:
            result = session.write_transaction(self._get_movies, skip=skip, limit=limit, order_field=order_field,
                                               order_direction=order_direction)
            return result

    def _get_movies(self, tx, skip: int = 0, limit: int = 10, order_field: str = "title",
                    order_direction: str = "ASC"):
        order_by = f"m.{order_field} {order_direction}"
        result = tx.run(
            f"MATCH (m:Title) <- [:ACTED_IN] - (a) return m as movie, collect(a) as actors ORDER BY {order_by} SKIP {skip} LIMIT {limit}")
        data = result.data()
        return data
