from typing import Protocol

from sqlalchemy.orm.query import Query


class QueryIncluderInterface(Protocol):
    """
    Interface that defines which methods each QueryIncluder needs to define.
    """

    def apply(self, query: Query) -> Query:
        """
        Accepts query of some DB model, joins specific entities to it and
        returns decorated query.
        """
