import faker
from uuid import uuid4
from typing import Optional

import inject

from app.db import User, Post, Comment, Tag, PostStatusType

generator = faker.Factory.create()


class UserMockPrecondition:

    @staticmethod
    def _default() -> dict:
        return {
            "first_name": generator.slug(),
            "last_name": generator.slug(),
            "email": generator.email(),
        }

    def exists(self, **kwargs) -> User:
        default_data = self._default()
        if kwargs:
            default_data.update(kwargs)
        db = inject.instance("db")
        user = User(**default_data)
        db.add(user)
        db.commit()
        return user


class PostMockPrecondition:
    @staticmethod
    def _default() -> dict:
        return {
            "user_id": uuid4(),
            "title": generator.slug(),
            "content": generator.text(),
            "status": PostStatusType.DRAFT
        }

    def exists(
        self,
        tags: Optional[list[Tag]] = None,
        **kwargs
    ) -> Post:
        default_data = self._default()
        if kwargs:
            default_data.update(kwargs)
        db = inject.instance("db")
        post = Post(**default_data)
        if tags is not None:
            post.tags.extend(tags)
        db.add(post)
        db.commit()
        return post


class CommentMockPrecondition:

    @staticmethod
    def _default() -> dict:
        return {
            "user_id": uuid4(),
            "post_id": uuid4(),
            "content": generator.text(),
            "name": generator.slug(),
        }

    def exists(self, **kwargs) -> Comment:
        default_data = self._default()
        if kwargs:
            default_data.update(kwargs)
        db = inject.instance("db")
        comment = Comment(**default_data)
        db.add(comment)
        db.commit()
        return comment


class TagMockPrecondition:

    @staticmethod
    def _default() -> dict:
        return {
            "slug": generator.slug()
        }

    def exists(self, **kwargs) -> Tag:
        default_data = self._default()
        if kwargs:
            default_data.update(kwargs)
        db = inject.instance("db")
        tag = Tag(**default_data)
        db.add(tag)
        db.commit()
        return tag
