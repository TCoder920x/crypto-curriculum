"""OpenAI utilities for managing assistants and vector stores"""
from typing import Optional, Dict, Any
import logging
from openai import AsyncOpenAI
from sqlalchemy import update, inspect
from sqlalchemy.exc import InvalidRequestError

from app.backend.core.config import settings
from app.backend.models.user import User

logger = logging.getLogger(__name__)

# Initialize OpenAI client
_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    """Get or create OpenAI client instance"""
    global _client
    if _client is None:
        api_key = settings.OPENAI_API_KEY
        if not api_key or api_key.strip() == "":
            raise ValueError("OPENAI_API_KEY is not set in configuration. Please set it in your .env file.")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def get_or_create_user_assistant(user: User, db=None) -> str:
    """
    Get or create a user-specific OpenAI assistant.
    
    Args:
        user: User object
        db: Optional database session to save assistant_id
    
    Returns:
        Assistant ID
    """
    client = get_openai_client()
    
    # Check if user already has an assistant
    if user.openai_assistant_id:
        try:
            # Verify assistant still exists
            assistant = await client.beta.assistants.retrieve(user.openai_assistant_id)
            return assistant.id
        except Exception as e:
            logger.warning(f"User assistant {user.openai_assistant_id} not found, creating new one: {e}")
    
    # Create new assistant
    assistant = await client.beta.assistants.create(
        name=f"Learning Assistant for {user.username or user.email}",
        instructions="You are a helpful learning assistant for blockchain and cryptocurrency education.",
        model="gpt-4.1-mini",  # Using gpt-4.1-mini model
        tools=[],  # Can add tools like web search later
    )
    
    # Store assistant ID in user model
    user.openai_assistant_id = assistant.id
    
    # Save to database if session provided
    if db:
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(openai_assistant_id=assistant.id)
        )
        await db.commit()
        try:
            user_state = inspect(user)
            if user_state.persistent:
                await db.refresh(user)
            else:
                refreshed_user = await db.get(User, user.id)
                if refreshed_user:
                    user.openai_assistant_id = refreshed_user.openai_assistant_id
        except InvalidRequestError as refresh_err:
            logger.warning(f"Could not refresh user {user.id} after assistant creation: {refresh_err}")
        except Exception as refresh_err:  # pragma: no cover
            logger.warning(f"Unexpected error refreshing user {user.id}: {refresh_err}")
    
    return assistant.id


async def get_or_create_user_vector_store(user: User) -> Optional[str]:
    """
    Get or create a user-specific vector store for RAG (optional feature).
    
    Returns:
        Vector store ID or None if not using vector stores
    """
    # For now, we'll skip vector stores as they're optional
    # Can be implemented later if needed for curriculum content retrieval
    return None


async def update_user_assistant_instructions(
    user: User,
    instructions: str
) -> str:
    """
    Update user assistant's instructions with context.
    
    Args:
        user: User object
        instructions: New instructions to set
    
    Returns:
        Updated assistant ID
    """
    client = get_openai_client()
    assistant_id = await get_or_create_user_assistant(user)
    
    await client.beta.assistants.update(
        assistant_id,
        instructions=instructions
    )
    
    return assistant_id


async def get_global_assistant_id() -> Optional[str]:
    """
    Get the global fallback assistant ID from config.
    Validates that the assistant exists before returning it.
    
    Returns:
        Assistant ID or None if not configured or doesn't exist
    """
    assistant_id = settings.OPENAI_ASSISTANT_ID
    if not assistant_id or not assistant_id.strip():
        return None
    
    assistant_id = assistant_id.strip()
    
    # Validate that the assistant exists
    try:
        client = get_openai_client()
        await client.beta.assistants.retrieve(assistant_id)
        return assistant_id
    except Exception as e:
        logger.warning(f"Global assistant {assistant_id} not found or invalid: {e}")
        return None


async def get_assistant_for_user(user: User, db=None) -> str:
    """
    Get assistant ID for user, falling back to global assistant if needed.
    
    Args:
        user: User object
        db: Optional database session
    
    Returns:
        Assistant ID
    """
    # First check if global assistant is configured and valid - use it if available
    global_id = await get_global_assistant_id()
    if global_id:
        logger.info(f"Using validated global assistant: {global_id}")
        return global_id
    
    # Otherwise, try to get or create user-specific assistant
    try:
        logger.info(f"Creating/getting user-specific assistant for user {user.id}")
        return await get_or_create_user_assistant(user, db)
    except Exception as e:
        logger.error(f"Error getting user assistant: {e}", exc_info=True)
        # Try global assistant one more time as fallback
        global_id = await get_global_assistant_id()
        if global_id:
            logger.warning(f"Falling back to global assistant due to error: {e}")
            return global_id
        raise ValueError(f"No assistant available. Error: {str(e)}. Please configure OPENAI_API_KEY. If using OPENAI_ASSISTANT_ID, ensure it exists in your OpenAI account.")


async def cancel_active_run(thread_id: str, run_id: str) -> None:
    """
    Cancel an active OpenAI run.
    
    Args:
        thread_id: OpenAI thread ID
        run_id: OpenAI run ID
    """
    try:
        client = get_openai_client()
        await client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
        logger.info(f"Cancelled run {run_id} for thread {thread_id}")
    except Exception as e:
        logger.warning(f"Error cancelling run {run_id}: {e}")


async def list_active_runs(thread_id: str) -> list[Dict[str, Any]]:
    """
    List active runs for a thread.
    
    Args:
        thread_id: OpenAI thread ID
    
    Returns:
        List of active run objects
    """
    try:
        client = get_openai_client()
        runs = await client.beta.threads.runs.list(thread_id=thread_id, limit=10)
        active_runs = [run for run in runs.data if run.status in ["queued", "in_progress"]]
        return [{"id": run.id, "status": run.status} for run in active_runs]
    except Exception as e:
        logger.warning(f"Error listing runs for thread {thread_id}: {e}")
        return []

