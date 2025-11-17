#!/usr/bin/env python3
"""
Backfill OpenAI assistants for existing users.

This script creates OpenAI assistants for all users who don't have one yet,
as if they were created during registration.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = BASE_DIR / "app" / "backend" / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Try alternative location
    load_dotenv(BASE_DIR / ".env")

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
import logging

from app.backend.core.config import settings
from app.backend.core.openai_utils import get_or_create_user_assistant
from app.backend.models.user import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def create_assistants_for_users():
    """Create OpenAI assistants for all users without one"""
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    try:
        async with async_session() as db:
            # Get all users without an assistant
            result = await db.execute(
                select(User).where(
                    (User.openai_assistant_id.is_(None)) | (User.openai_assistant_id == "")
                )
            )
            users = result.scalars().all()
            
            if not users:
                logger.info("All users already have assistants assigned.")
                return
            
            logger.info(f"Found {len(users)} users without assistants. Creating assistants...")
            
            success_count = 0
            error_count = 0
            
            for user in users:
                # Store user info before any operations that might expire the object
                user_id = user.id
                user_email = user.email
                
                try:
                    assistant_id = await get_or_create_user_assistant(user, db)
                    logger.info(f"✓ Created assistant {assistant_id} for user {user_id} ({user_email})")
                    success_count += 1
                except Exception as e:
                    logger.error(f"✗ Failed to create assistant for user {user_id} ({user_email}): {e}")
                    error_count += 1
                    try:
                        await db.rollback()
                    except Exception:
                        pass
                    continue
            
            logger.info(f"\nSummary:")
            logger.info(f"  Successfully created: {success_count} assistants")
            if error_count > 0:
                logger.warning(f"  Failed: {error_count} users")
            
    except Exception as e:
        logger.error(f"Error creating assistants: {e}", exc_info=True)
        raise
    finally:
        await engine.dispose()


async def main():
    """Main entry point"""
    logger.info("Starting assistant creation for existing users...")
    logger.info(f"Database: {settings.DATABASE_URL}")
    
    try:
        await create_assistants_for_users()
        logger.info("Assistant creation complete!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

