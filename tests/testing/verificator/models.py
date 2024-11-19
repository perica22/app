from app.db import User, Post, Comment, Tag
from tests.testing.verificator.base import Verificator


# noinspection PyMethodMayBeStatic
class UserVerificator(Verificator):
    """User Verificator class"""

    def check_user_info(
        self, response_data: dict, mocked_data: User
    ) -> None:
        """
        Extracts data from response and verifies it by comparing it with
        provided values.
        """
        assert response_data["id"] == str(mocked_data.id)
        assert response_data["first_name"] == str(mocked_data.first_name)
        assert response_data["last_name"] == str(mocked_data.last_name)
        assert response_data["email"] == str(mocked_data.email)


# noinspection PyMethodMayBeStatic
class PostVerificator(Verificator):
    """Post Verificator class"""

    def check_post_info(
        self, response_data: dict, mocked_data: Post
    ) -> None:
        """
        Extracts data from response and verifies it by comparing it with
        provided values.
        """
        assert response_data["id"] == str(mocked_data.id)
        assert response_data["title"] == str(mocked_data.title)
        assert response_data["content"] == str(mocked_data.content)
        assert response_data["status"] == str(mocked_data.status.value)

    def check_posts_info(
        self, response_data: list[dict], mocked_data: list[Post]
    ) -> None:
        mocked_posts_map: dict[str, Post] = {
            str(post.id): post for post in mocked_data
        }
        for post in response_data:
            self.check_post_info(
                response_data=post,
                mocked_data=mocked_posts_map[post["id"]]
            )


# noinspection PyMethodMayBeStatic
class CommentVerificator(Verificator):
    """Comment Verificator class"""

    def check_comment_info(
        self, response_data: dict, mocked_data: Comment
    ) -> None:
        """
        Extracts data from response and verifies it by comparing it with
        provided values.
        """
        assert response_data["id"] == str(mocked_data.id)
        assert response_data["user_id"] == str(mocked_data.user_id)
        assert response_data["post_id"] == str(mocked_data.post_id)
        assert response_data["content"] == str(mocked_data.content)

    def check_comments_info(
        self, response_data: list[dict], mocked_data: list[Comment]
    ) -> None:
        mocked_comments_map: dict[str, Comment] = {
            str(comment.id): comment for comment in mocked_data
        }
        for comment in response_data:
            self.check_comment_info(
                response_data=comment,
                mocked_data=mocked_comments_map[comment["id"]]
            )


# noinspection PyMethodMayBeStatic
class TagVerificator(Verificator):
    """Tag Verificator class"""

    def check_tag_info(
        self, response_data: dict, mocked_data: Tag
    ) -> None:
        """
        Extracts data from response and verifies it by comparing it with
        provided values.
        """
        assert response_data["id"] == str(mocked_data.id)
        assert response_data["slug"] == str(mocked_data.slug)

    def check_tags_info(
        self, response_data: list[dict], mocked_data: list[Tag]
    ) -> None:
        mocked_tags_map: dict[str, Tag] = {
            str(tag.id): tag for tag in mocked_data
        }
        for tag in response_data:
            self.check_tag_info(
                response_data=tag,
                mocked_data=mocked_tags_map[tag["id"]]
            )
