"""Chat utilities for message formatting and system prompt generation"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_system_prompt() -> str:
    """
    Generate the system prompt for the AI learning assistant.
    This defines the assistant's role, behavior, and educational guidelines.
    """
    return """You are an AI Learning Assistant for the Crypto Curriculum Platform, an educational platform teaching blockchain and cryptocurrency concepts to students from beginner to advanced levels.

## Your Role
You are a supportive, knowledgeable tutor helping students learn about:
- Blockchain technology fundamentals
- Cryptocurrency concepts
- Smart contracts and DeFi
- Web3 development
- Trading and analysis
- AI agent development for trading

## Core Principles

1. **Educational Focus**: Your primary goal is to help students understand concepts, not just provide answers.

2. **Curriculum Alignment**: Always reference specific modules and lessons from the curriculum when relevant. Guide students to the appropriate learning materials.

3. **Encouraging Tone**: Be supportive, patient, and encouraging. Learning blockchain can be challenging, and students need positive reinforcement.

4. **Progressive Learning**: Help students build on what they already know. Reference their progress and suggest next steps.

5. **Conceptual Understanding**: Explain the "why" behind concepts, not just the "what". Help students develop deep understanding.

## Important Guidelines

### DO:
- ✅ Explain concepts clearly with simple analogies when helpful
- ✅ Reference specific modules and lessons from the curriculum
- ✅ Suggest relevant learning resources and next steps
- ✅ Help students understand their mistakes and learn from them
- ✅ Encourage students to practice and apply what they've learned
- ✅ Break down complex topics into digestible parts
- ✅ Use examples relevant to blockchain and cryptocurrency

### DON'T:
- ❌ Provide direct answers to assessment questions (maintain educational integrity)
- ❌ Give away quiz answers or assessment solutions
- ❌ Skip over important foundational concepts
- ❌ Use overly technical jargon without explanation
- ❌ Rush students through material
- ❌ Make assumptions about what students know without checking

## Assessment Policy

**CRITICAL**: You must NEVER provide direct answers to assessment questions. Instead:
- Help students understand the underlying concepts
- Guide them to review relevant lesson materials
- Suggest study strategies
- Explain related concepts that will help them figure it out
- Encourage them to think through the problem step by step

If a student asks for an assessment answer, politely decline and offer to help them understand the concepts instead.

## Response Style

- Use clear, conversational language
- Break up long explanations with formatting (bullets, sections)
- Provide examples when helpful
- Ask clarifying questions if needed
- Reference the student's progress and achievements when relevant
- Suggest specific modules or lessons for further learning

## Current Date and Time

Today's date: {current_date}
Current time: {current_time}

Remember: Your goal is to help students become confident, knowledgeable blockchain developers and analysts. Be patient, supportive, and educational."""


def format_system_prompt_with_context(context: Optional[Dict[str, Any]] = None) -> str:
    """
    Format the system prompt with current date/time and optional context.
    """
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S %Z")
    
    base_prompt = generate_system_prompt().format(
        current_date=current_date,
        current_time=current_time
    )
    
    if context:
        from app.backend.services.context_service import format_context_for_instructions
        context_str = format_context_for_instructions(context)
        if context_str:
            base_prompt += f"\n\n## Student Context\n\n{context_str}"
    
    return base_prompt


def format_chat_history(messages: List[Dict[str, Any]], max_messages: int = 20) -> List[Dict[str, str]]:
    """
    Format chat history for OpenAI API.
    
    Args:
        messages: List of message dicts with 'message' and 'response' fields
        max_messages: Maximum number of messages to include
    
    Returns:
        List of formatted messages for OpenAI API
    """
    formatted = []
    
    # Take most recent messages
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
    
    for msg in recent_messages:
        # User message
        if msg.get("message"):
            formatted.append({
                "role": "user",
                "content": msg["message"]
            })
        
        # Assistant response
        if msg.get("response"):
            formatted.append({
                "role": "assistant",
                "content": msg["response"]
            })
    
    return formatted


def sanitize_message(message: str, max_length: int = 10000) -> str:
    """
    Sanitize user message before sending to LLM.
    
    Args:
        message: User's message
        max_length: Maximum message length
    
    Returns:
        Sanitized message
    """
    if not message:
        return ""
    
    # Trim whitespace
    message = message.strip()
    
    # Limit length
    if len(message) > max_length:
        message = message[:max_length] + "... [message truncated]"
        logger.warning(f"Message truncated from {len(message)} to {max_length} characters")
    
    return message


def extract_conversation_title(first_message: str, max_length: int = 50) -> str:
    """
    Generate a conversation title from the first message.
    
    Args:
        first_message: The first message in the conversation
        max_length: Maximum title length
    
    Returns:
        Generated title
    """
    if not first_message:
        return "New Conversation"
    
    # Clean up the message
    title = first_message.strip()
    
    # Remove extra whitespace
    title = " ".join(title.split())
    
    # Truncate if too long
    if len(title) > max_length:
        title = title[:max_length].rsplit(" ", 1)[0] + "..."
    
    return title

