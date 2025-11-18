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


async def format_citations_in_response(
    response_text: str,
    db: Optional[Any] = None
) -> str:
    """
    Replace OpenAI citation format with readable document names.
    
    OpenAI citations come in format: 【8:0+filename.txt】
    This function replaces them with: [Document: "title"]
    
    Args:
        response_text: Response text containing citations
        db: Optional database session for document lookup
    
    Returns:
        Response text with formatted citations
    """
    import re
    from pathlib import Path
    
    if not response_text:
        return response_text
    
    if not db:
        logger.warning("format_citations_in_response called without database session")
        return response_text
    
    citation_pattern = r'【(\d+:\d+)\+([^】]+)】'
    matches = list(re.finditer(citation_pattern, response_text))
    
    if not matches:
        return response_text
    
    logger.info(f"Found {len(matches)} citation(s) to format in response")
    
    from sqlalchemy import select
    from app.backend.models.document import Document
    
    replacements = {}
    
    for match in matches:
        citation_ref = match.group(1)
        filename = match.group(2)
        
        if filename in replacements:
            continue
        
        try:
            filename_clean = filename.strip()
            filename_base = Path(filename_clean).stem
            filename_with_path = f"/{filename_clean}"
            filename_in_storage = f"storage/documents/{filename_clean}"
            
            result = await db.execute(
                select(Document)
                .where(Document.is_deleted == False)
                .where(
                    (Document.filename == filename_clean) |
                    (Document.filename.like(f"%{filename_base}%")) |
                    (Document.storage_path.like(f"%{filename_clean}%")) |
                    (Document.storage_path.like(f"%{filename_with_path}%")) |
                    (Document.storage_path.like(f"%{filename_in_storage}%")) |
                    (Document.storage_path.endswith(filename_clean))
                )
                .limit(1)
            )
            document = result.scalar_one_or_none()
            
            if document:
                replacements[filename] = f'[Document: "{document.title}"]'
                logger.info(f"Replaced citation {filename} with document title: {document.title}")
            else:
                display_name = filename_base if filename_base else filename_clean
                replacements[filename] = f'[Document: "{display_name}"]'
                logger.warning(f"Document not found for citation {filename}, using fallback: {display_name}")
        except Exception as e:
            logger.error(f"Error looking up citation {filename}: {e}", exc_info=True)
            display_name = Path(filename).stem if filename else filename
            replacements[filename] = f'[Document: "{display_name}"]'
    
    def replace_match(match):
        filename = match.group(2)
        replacement = replacements.get(filename, f'[Document: "{filename}"]')
        return replacement
    
    formatted_text = re.sub(citation_pattern, replace_match, response_text)
    
    if formatted_text == response_text and len(matches) > 0:
        logger.error("Citation pattern matched but text was not modified - forcing replacement")
        def simple_replace(m):
            fn = m.group(2)
            return f'[Document: "{Path(fn).stem}"]'
        formatted_text = re.sub(citation_pattern, simple_replace, response_text)
    
    if len(replacements) > 0:
        logger.info(f"Formatted {len(replacements)} citation(s) in response")
    
    return formatted_text

