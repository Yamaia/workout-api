from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def commit_or_conflict(session: AsyncSession, mensagem: str) -> None:
    """Confirma a transação; em `IntegrityError` devolve 303 com a mensagem informada."""
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=mensagem)
