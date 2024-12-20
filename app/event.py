from fastapi import Response, Request


class Event:
    """
    Simple class for holding audit event ID and description.
    """
    def __init__(self, id: str, description: str) -> None:
        self.id = id
        self.description = description

    @classmethod
    def from_error(cls, response: Response, request: Request) -> "Event":
        return Event(
            id=str(response.status_code),
            description=f"Error occurred on route {str(request.url)}"
        )


GET_USER = Event(
    "GetUser", "Get user details"
)
GET_POST = Event(
    "GetPost", "Get post details"
)
LIST_POSTS = Event(
    "ListPosts", "List posts details"
)
