"""Re-seed assessments with proper questions (clears existing assessments first)"""
import asyncio
from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.database import AsyncSessionLocal
from app.backend.models.assessment import Assessment
from app.backend.models.module import Module
from app.backend.seed_local import seed_assessments, seed_modules_lessons


async def clear_assessments(session: AsyncSession) -> None:
    """Clear all existing assessments"""
    await session.execute(delete(Assessment))
    await session.flush()
    print("✓ Cleared all existing assessments")


async def main() -> None:
    """Clear and re-seed assessments with proper questions"""
    async with AsyncSessionLocal() as session:
        print("Clearing existing assessments...")
        await clear_assessments(session)
        
        print("Fetching modules...")
        # Get all modules (they should already exist)
        from sqlalchemy import select
        result = await session.execute(select(Module))
        modules = result.scalars().all()
        
        if not modules:
            print("No modules found. Seeding modules first...")
            modules = await seed_modules_lessons(session)
            await session.commit()
            print(f"✓ Created {len(modules)} modules")
        
        print(f"Re-seeding assessments for {len(modules)} modules...")
        await seed_assessments(session, modules)
        
        await session.commit()
        
        # Realign sequence so future inserts don't collide
        await session.execute(
            text(
                "SELECT setval('assessments_id_seq', "
                "(SELECT COALESCE(MAX(id), 0) FROM assessments) + 1, false)"
            )
        )
        await session.execute(
            text(
                "SELECT setval('quiz_attempts_id_seq', "
                "(SELECT COALESCE(MAX(id), 0) FROM quiz_attempts) + 1, false)"
            )
        )
        await session.commit()
        print("✓ Reset assessment ID sequence")
        print("✓ Successfully re-seeded all assessments with proper questions")
        print(f"✓ Module 1 now has 10 multiple choice questions")


if __name__ == "__main__":
    asyncio.run(main())

