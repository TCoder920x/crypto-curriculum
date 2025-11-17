"""Context service for gathering user-specific learning data for AI assistant"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from app.backend.models.user import User
from app.backend.models.progress import UserProgress, QuizAttempt
from app.backend.models.module import Module
from app.backend.models.assessment import Assessment
from app.backend.models.achievement import UserAchievement, Achievement
from app.backend.models.forum import ForumPost

logger = logging.getLogger(__name__)


async def gather_user_context(
    user: User,
    db: AsyncSession,
    current_module_id: Optional[int] = None,
    current_lesson_id: Optional[int] = None,
    extra_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Gather user-specific learning context for AI assistant.
    
    Only includes information specific to this user for privacy and security.
    """
    context = {
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role.value if user.role else "student",
        },
        "current_context": {},
        "progress": [],
        "available_modules": [],
        "recent_assessments": [],
        "achievements": [],
        "recent_forum_activity": [],
        "calendar_events": [],
        "notes": [],
        "assignments": [],
    }
    
    try:
        # Current module/lesson context
        if current_module_id:
            context["current_context"]["module_id"] = current_module_id
        if current_lesson_id:
            context["current_context"]["lesson_id"] = current_lesson_id
        
        # Get user's progress across all modules
        progress_result = await db.execute(
            select(UserProgress)
            .where(UserProgress.user_id == user.id)
            .order_by(UserProgress.last_accessed_at.desc())
        )
        user_progress = progress_result.scalars().all()
        
        context["progress"] = [
            {
                "module_id": p.module_id,
                "status": p.status.value if p.status else "not_started",
                "completion_percentage": p.completion_percentage,
                "last_accessed": p.last_accessed_at.isoformat() if p.last_accessed_at else None,
                "started_at": p.started_at.isoformat() if p.started_at else None,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None,
            }
            for p in user_progress
        ]
        
        # Get all available modules for context
        modules_result = await db.execute(
            select(Module)
            .where(Module.is_published == True)
            .order_by(Module.order_index)
        )
        all_modules = modules_result.scalars().all()
        
        context["available_modules"] = [
            {
                "id": m.id,
                "title": m.title,
                "track": m.track.value if m.track else None,
                "order_index": m.order_index,
                "description": m.description,
                "duration_hours": m.duration_hours,
                "learning_objectives": m.learning_objectives,
            }
            for m in all_modules
        ]
        
        # Get recent assessment attempts (last 20)
        recent_attempts_result = await db.execute(
            select(QuizAttempt, Assessment)
            .join(Assessment, QuizAttempt.assessment_id == Assessment.id)
            .where(QuizAttempt.user_id == user.id)
            .order_by(desc(QuizAttempt.attempted_at))
            .limit(20)
        )
        recent_attempts = recent_attempts_result.all()
        
        context["recent_assessments"] = [
            {
                "assessment_id": attempt.assessment_id,
                "module_id": assessment.module_id,
                "question_type": assessment.question_type.value if assessment.question_type else None,
                "is_correct": attempt.is_correct,
                "points_earned": attempt.points_earned,
                "review_status": attempt.review_status.value if attempt.review_status else None,
                "feedback": attempt.feedback,
                "attempted_at": attempt.attempted_at.isoformat() if attempt.attempted_at else None,
            }
            for attempt, assessment in recent_attempts
        ]
        
        # Get earned achievements
        achievements_result = await db.execute(
            select(UserAchievement, Achievement)
            .join(Achievement, UserAchievement.achievement_id == Achievement.id)
            .where(UserAchievement.user_id == user.id)
            .order_by(desc(UserAchievement.earned_at))
        )
        user_achievements = achievements_result.all()
        
        context["achievements"] = [
            {
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "category": achievement.category,
                "points": achievement.points,
                "earned_at": user_achievement.earned_at.isoformat() if user_achievement.earned_at else None,
            }
            for user_achievement, achievement in user_achievements
        ]
        
        # Get recent forum activity (last 10 posts user created or participated in)
        forum_posts_result = await db.execute(
            select(ForumPost)
            .where(ForumPost.user_id == user.id)
            .order_by(desc(ForumPost.created_at))
            .limit(10)
        )
        recent_posts = forum_posts_result.scalars().all()
        
        context["recent_forum_activity"] = [
            {
                "post_id": post.id,
                "module_id": post.module_id,
                "title": post.title,
                "content_preview": post.content[:200] if post.content else None,  # First 200 chars
                "is_solved": post.is_solved,
                "upvotes": post.upvotes,
                "created_at": post.created_at.isoformat() if post.created_at else None,
            }
            for post in recent_posts
        ]

        # Merge any additional context provided by the caller (e.g., LMS calendar/notes)
        if extra_context:
            context["calendar_events"] = extra_context.get("calendar_events", []) or extra_context.get("calendar", [])
            context["notes"] = extra_context.get("notes", [])
            context["assignments"] = extra_context.get("assignments", []) or extra_context.get("tasks", [])
            if extra_context.get("additional_instructions"):
                context["additional_instructions"] = extra_context["additional_instructions"]
        
    except Exception as e:
        logger.error(f"Error gathering user context for user {user.id}: {str(e)}")
        # Continue with partial context rather than failing completely
    
    return context


def format_context_for_instructions(context: Dict[str, Any]) -> str:
    """
    Format user context into a string for OpenAI assistant instructions.
    """
    parts = []
    
    # User info
    user_info = context.get("user", {})
    parts.append(f"Student: {user_info.get('username', 'Unknown')} (ID: {user_info.get('id')})")
    parts.append(f"Role: {user_info.get('role', 'student')}")
    
    # Current context
    current = context.get("current_context", {})
    if current.get("module_id"):
        parts.append(f"\nCurrently viewing: Module {current.get('module_id')}")
        if current.get("lesson_id"):
            parts.append(f"Lesson: {current.get('lesson_id')}")
    
    # Progress summary
    progress = context.get("progress", [])
    if progress:
        parts.append("\n## Learning Progress:")
        completed = [p for p in progress if p.get("status") == "completed"]
        in_progress = [p for p in progress if p.get("status") == "in_progress"]
        
        if completed:
            parts.append(f"- Completed modules: {len(completed)}")
        if in_progress:
            parts.append(f"- In progress modules: {len(in_progress)}")
            for p in in_progress[:3]:  # Show top 3
                parts.append(f"  * Module {p.get('module_id')}: {p.get('completion_percentage', 0):.0f}% complete")
    
    # Available modules
    modules = context.get("available_modules", [])
    if modules:
        parts.append(f"\n## Available Curriculum:")
        parts.append(f"Total modules: {len(modules)}")
        # Group by track
        tracks = {}
        for m in modules:
            track = m.get("track", "Unknown")
            if track not in tracks:
                tracks[track] = []
            tracks[track].append(m)
        
        for track, track_modules in tracks.items():
            parts.append(f"- {track} track: {len(track_modules)} modules")
    
    # Recent assessment performance
    assessments = context.get("recent_assessments", [])
    if assessments:
        parts.append("\n## Recent Assessment Performance:")
        correct = sum(1 for a in assessments if a.get("is_correct") is True)
        total = len(assessments)
        if total > 0:
            parts.append(f"Recent accuracy: {correct}/{total} ({100*correct/total:.0f}%)")
        
        # Areas needing improvement
        incorrect = [a for a in assessments if a.get("is_correct") is False]
        if incorrect:
            parts.append(f"Areas to review: {len(incorrect)} recent incorrect answers")
    
    # Achievements
    achievements = context.get("achievements", [])
    if achievements:
        parts.append(f"\n## Achievements Earned: {len(achievements)}")
        recent_achievements = achievements[:5]  # Show 5 most recent
        for ach in recent_achievements:
            parts.append(f"- {ach.get('name')}: {ach.get('description', '')}")

    # Assignments
    assignments = context.get("assignments", [])
    if assignments:
        parts.append(f"\n## Upcoming Assignments: {len(assignments)}")
        for item in assignments[:5]:
            if isinstance(item, dict):
                title = item.get("title") or item.get("name") or "Assignment"
                due = item.get("due_date") or item.get("due") or item.get("deadline")
                parts.append(f"- {title}" + (f" (due {due})" if due else ""))
            else:
                parts.append(f"- {item}")

    # Notes
    notes = context.get("notes", [])
    if notes:
        parts.append(f"\n## Notes & Highlights: {len(notes)}")
        for note in notes[:3]:
            if isinstance(note, dict):
                snippet = note.get("summary") or note.get("content") or note.get("text") or ""
            else:
                snippet = str(note)
            trimmed = (snippet[:180] + "...") if len(snippet) > 180 else snippet
            parts.append(f"- {trimmed}")

    # Calendar events
    calendar_events = context.get("calendar_events", [])
    if calendar_events:
        parts.append(f"\n## Calendar Events: {len(calendar_events)}")
        for event in calendar_events[:5]:
            if isinstance(event, dict):
                title = event.get("title") or event.get("name") or "Event"
                when = event.get("start") or event.get("date") or event.get("starts_at")
                parts.append(f"- {title}" + (f" on {when}" if when else ""))
            else:
                parts.append(f"- {event}")
    
    # Forum activity
    forum_activity = context.get("recent_forum_activity", [])
    if forum_activity:
        parts.append(f"\n## Recent Forum Activity: {len(forum_activity)} posts")

    if context.get("additional_instructions"):
        parts.append("\n## Additional Context:")
        parts.append(str(context.get("additional_instructions")))
    
    return "\n".join(parts)
