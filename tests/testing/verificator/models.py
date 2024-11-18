from app.db import User, Post
from tests.testing.verificator.base import Verificator


# noinspection PyMethodMayBeStatic
class UserVerificator(Verificator):
    """User Verificator class"""

    def check_user_info(
        self, response_data: dict, mocked_user: User
    ) -> None:
        """
        Extracts data from response and verifies it by comparing it with
        provided values.
        """
        assert response_data["id"] == str(mocked_user.id)
        assert response_data["first_name"] == str(mocked_user.first_name)
        assert response_data["last_name"] == str(mocked_user.last_name)
        assert response_data["email"] == str(mocked_user.email)


# noinspection PyMethodMayBeStatic
class PostVerificator(Verificator):
    """Post Verificator class"""

    def check_post_info(
        self, response_data: dict, mocked_post: Post
    ) -> None:
        """
        Extracts data from response and verifies it by comparing it with
        provided values.
        """
        assert response_data["id"] == str(mocked_post.id)
        assert response_data["title"] == str(mocked_post.title)
        assert response_data["content"] == str(mocked_post.content)
        assert response_data["status"] == str(mocked_post.status.value)

    def check_posts_info(
        self, response_data: list[dict], mocked_posts: list[Post]
    ) -> None:
        mocked_posts_map: dict[str, Post] = {
            str(post.id): post for post in mocked_posts
        }
        for post in response_data:
            self.check_post_info(
                response_data=post,
                mocked_post=mocked_posts_map[post["id"]]
            )
