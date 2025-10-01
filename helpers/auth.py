from fastapi import Depends, HTTPException, status, Header
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from models.auth import Token, Agent, TokenUser, TokenAgent, User
from database import get_session
from datetime import datetime, timezone


async def get_auth_token(
    authorization: str = Header(),
    db_session: Session = Depends(get_session)
) -> Token:
    """Extract and validate token from Authorization header, returning Token object with relationships loaded."""

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    token_string = authorization.split(" ")[1]

    # Single query with joins to load Token with User and Agent relationships
    statement = (
        select(Token)
        .options(
            joinedload(Token.token_users).joinedload(TokenUser.user),
            joinedload(Token.token_agents).joinedload(TokenAgent.agent)
        )
        .where(
            Token.access_token == token_string,
            Token.is_revoked == False,
            Token.expires_at > datetime.now(timezone.utc)
        )
    )

    token = db_session.exec(statement).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return token


def get_user_from_token(token: Token, db_session: Session = None) -> User | None:
    """Get user associated with a token (using preloaded relationship)."""
    return token.user


async def require_user_or_agent(
    token: Token,
    db_session: Session = None
) -> None:
    """Validate that the token is associated with either a user or an agent. Raises 403 if neither."""

    # Token must be associated with either a user or agent
    if not token.user and not token.agent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Valid user or agent authentication required"
        )

    # If it's a user, they must be active
    if token.user and not token.user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # If it's an agent, they must be active
    if token.agent and not token.agent.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent is inactive"
        )
