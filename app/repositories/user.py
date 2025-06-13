from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only, selectinload

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user(
        self,
        field: str,
        value: Any,
        selected_fields: Optional[list[str]] = None,
        include_relations: Optional[list[str]] = None,
    ) -> User:
        query = select(User).filter(getattr(User, field) == value)
        if selected_fields:
            orm_fields = [getattr(User, field) for field in selected_fields]
            # Always include a primary key
            orm_fields.append(User.id)
            query = query.options(load_only(*orm_fields))

        # Add relationships if requested
        if include_relations:
            for relation in include_relations:
                if hasattr(User, relation):
                    query = query.options(selectinload(getattr(User, relation)))

        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_user(
        self, user: User, selected_fields: Optional[list[str]] = None
    ) -> User:
        self.session.add(user)
        await self.session.commit()
        # Refresh only selected fields
        await self.session.refresh(user, attribute_names=selected_fields)
        return user

    async def update_user(
        self, user: User, data: dict, selected_fields: list[str]
    ) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user, attribute_names=selected_fields)
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
