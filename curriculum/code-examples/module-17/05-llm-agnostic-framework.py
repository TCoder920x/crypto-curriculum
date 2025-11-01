"""
Module 17.10: LLM-Agnostic Framework Implementation
Complete framework for working with any LLM provider

This framework allows you to switch between OpenAI, Anthropic, and local models
(Ollama) without changing your application code. Just update the configuration.

Features:
- Unified interface for all providers
- Tool calling system
- Cost tracking
- Conversation management
- Easy provider switching via config
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
import json
import yaml
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Message:
    """Unified message format across all providers"""
    role: str  # 'system', 'user', 'assistant', 'function'
    content: str


@dataclass
class Tool:
    """Tool definition for agent capabilities"""
    name: str
    description: str
    function: callable
    parameters: Dict[str, Any]


@dataclass
class AgentResponse:
    """Standardized response format"""
    content: str
    tool_calls: List[Dict] = None
    tokens_used: int = 0
    cost: float = 0.0
    latency_ms: float = 0.0
    provider: str = ""


# ============================================================================
# BASE AGENT (Abstract)
# ============================================================================

class BaseAgent(ABC):
    """
    Abstract base class for all LLM providers
    
    All providers must implement:
    - generate(): Send messages to LLM and get response
    - get_cost_per_token(): Return pricing information
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.model = config.get('model')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 1000)
        
        # Tool system
        self.tools: Dict[str, Tool] = {}
        
        # Conversation management
        self.conversation_history: List[Message] = []
        
        # Usage tracking
        self.total_tokens = 0
        self.total_cost = 0.0
    
    @abstractmethod
    async def generate(
        self, 
        messages: List[Message],
        tools: Optional[List[Tool]] = None
    ) -> AgentResponse:
        """Generate response from LLM - must be implemented by each provider"""
        pass
    
    @abstractmethod
    def get_cost_per_token(self) -> tuple[float, float]:
        """Return (input_cost_per_1k, output_cost_per_1k)"""
        pass
    
    def register_tool(self, tool: Tool):
        """Register a tool that the agent can use"""
        self.tools[tool.name] = tool
        logger.info(f"🔧 Registered tool: {tool.name}")
    
    async def chat(self, user_message: str, system_prompt: str = None) -> str:
        """
        Simple chat interface
        
        Args:
            user_message: User's message
            system_prompt: Optional system prompt
            
        Returns:
            Assistant's response
        """
        messages = []
        
        if system_prompt:
            messages.append(Message('system', system_prompt))
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add new user message
        messages.append(Message('user', user_message))
        
        # Generate response
        response = await self.generate(messages, list(self.tools.values()))
        
        # Update conversation history
        self.conversation_history.append(Message('user', user_message))
        self.conversation_history.append(Message('assistant', response.content))
        
        # Update usage tracking
        self.total_tokens += response.tokens_used
        self.total_cost += response.cost
        
        return response.content
    
    async def execute_with_tools(self, user_message: str, max_iterations: int = 5) -> AgentResponse:
        """
        Execute agent with tool calling loop
        
        The agent can call tools multiple times until it has enough
        information to provide a final answer.
        """
        messages = [Message('user', user_message)]
        
        for iteration in range(max_iterations):
            logger.info(f"Iteration {iteration + 1}/{max_iterations}")
            
            response = await self.generate(messages, list(self.tools.values()))
            
            # If no tool calls, we're done
            if not response.tool_calls:
                return response
            
            # Execute tool calls
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['arguments']
                
                if tool_name not in self.tools:
                    logger.warning(f"⚠️  Tool {tool_name} not found")
                    continue
                
                logger.info(f"🔧 Executing tool: {tool_name}({tool_args})")
                
                try:
                    result = await self.tools[tool_name].function(**tool_args)
                    messages.append(Message('function', f"{tool_name} result: {result}"))
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    messages.append(Message('function', f"{tool_name} error: {str(e)}"))
        
        # Max iterations reached without final answer
        return AgentResponse(
            content="Max iterations reached without final answer",
            provider=self.config.get('provider', 'unknown')
        )
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("🔄 Conversation history cleared")
    
    def get_stats(self) -> dict:
        """Get usage statistics"""
        return {
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost,
            'messages': len(self.conversation_history),
            'provider': self.config.get('provider')
        }


# ============================================================================
# OPENAI PROVIDER
# ============================================================================

class OpenAIAgent(BaseAgent):
    """OpenAI GPT implementation"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        
        # Import here to make it optional
        import openai
        self.client = openai.AsyncOpenAI(api_key=config['api_key'])
        
        # Pricing (as of Nov 2025 - verify current pricing)
        self.cost_per_1k = {
            'gpt-4': (0.03, 0.06),
            'gpt-4-turbo': (0.01, 0.03),
            'gpt-3.5-turbo': (0.001, 0.002)
        }
    
    async def generate(
        self, 
        messages: List[Message],
        tools: Optional[List[Tool]] = None
    ) -> AgentResponse:
        start_time = time.time()
        
        # Convert to OpenAI format
        openai_messages = [
            {'role': msg.role, 'content': msg.content}
            for msg in messages
        ]
        
        # Convert tools to OpenAI format
        openai_tools = None
        if tools:
            openai_tools = [
                {
                    'type': 'function',
                    'function': {
                        'name': tool.name,
                        'description': tool.description,
                        'parameters': tool.parameters
                    }
                }
                for tool in tools
            ]
        
        # API call
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            tools=openai_tools,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        latency = (time.time() - start_time) * 1000
        
        # Extract response
        choice = response.choices[0]
        content = choice.message.content or ""
        
        # Extract tool calls
        tool_calls = []
        if choice.message.tool_calls:
            tool_calls = [
                {
                    'name': tc.function.name,
                    'arguments': json.loads(tc.function.arguments)
                }
                for tc in choice.message.tool_calls
            ]
        
        # Calculate cost
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        input_cost, output_cost = self.cost_per_1k.get(self.model, (0, 0))
        cost = (input_tokens / 1000 * input_cost) + (output_tokens / 1000 * output_cost)
        
        return AgentResponse(
            content=content,
            tool_calls=tool_calls,
            tokens_used=total_tokens,
            cost=cost,
            latency_ms=latency,
            provider="OpenAI"
        )
    
    def get_cost_per_token(self) -> tuple[float, float]:
        return self.cost_per_1k.get(self.model, (0, 0))


# ============================================================================
# ANTHROPIC PROVIDER
# ============================================================================

class AnthropicAgent(BaseAgent):
    """Anthropic Claude implementation"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        
        # Import here to make it optional
        import anthropic
        self.client = anthropic.AsyncAnthropic(api_key=config['api_key'])
        
        # Pricing (as of Nov 2025 - verify current pricing)
        self.cost_per_1k = {
            'claude-3-5-sonnet-20241022': (0.003, 0.015),
            'claude-3-opus-20240229': (0.015, 0.075)
        }
    
    async def generate(
        self, 
        messages: List[Message],
        tools: Optional[List[Tool]] = None
    ) -> AgentResponse:
        start_time = time.time()
        
        # Separate system prompt (Anthropic requirement)
        system_prompt = ""
        anthropic_messages = []
        
        for msg in messages:
            if msg.role == 'system':
                system_prompt = msg.content
            else:
                anthropic_messages.append({
                    'role': msg.role,
                    'content': msg.content
                })
        
        # Convert tools to Anthropic format
        anthropic_tools = None
        if tools:
            anthropic_tools = [
                {
                    'name': tool.name,
                    'description': tool.description,
                    'input_schema': tool.parameters
                }
                for tool in tools
            ]
        
        # API call
        response = await self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=anthropic_messages,
            tools=anthropic_tools,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        latency = (time.time() - start_time) * 1000
        
        # Extract response
        content = ""
        tool_calls = []
        
        for block in response.content:
            if block.type == 'text':
                content += block.text
            elif block.type == 'tool_use':
                tool_calls.append({
                    'name': block.name,
                    'arguments': block.input
                })
        
        # Calculate cost
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens
        
        input_cost, output_cost = self.cost_per_1k.get(self.model, (0, 0))
        cost = (input_tokens / 1000 * input_cost) + (output_tokens / 1000 * output_cost)
        
        return AgentResponse(
            content=content,
            tool_calls=tool_calls,
            tokens_used=total_tokens,
            cost=cost,
            latency_ms=latency,
            provider="Anthropic"
        )
    
    def get_cost_per_token(self) -> tuple[float, float]:
        return self.cost_per_1k.get(self.model, (0, 0))


# ============================================================================
# OLLAMA PROVIDER (Local Models)
# ============================================================================

class OllamaAgent(BaseAgent):
    """Ollama local model implementation"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.cost_per_1k = (0, 0)  # Free (local)
    
    async def generate(
        self, 
        messages: List[Message],
        tools: Optional[List[Tool]] = None
    ) -> AgentResponse:
        start_time = time.time()
        
        # Import here to make it optional
        import httpx
        
        # Convert to Ollama format
        ollama_messages = [
            {'role': msg.role, 'content': msg.content}
            for msg in messages
        ]
        
        # Ollama doesn't have native tool support - inject into prompt
        if tools:
            tools_description = "\n\nAvailable tools:\n"
            for tool in tools:
                tools_description += f"- {tool.name}: {tool.description}\n"
            ollama_messages[0]['content'] += tools_description
        
        # API call
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    'model': self.model,
                    'messages': ollama_messages,
                    'stream': False,
                    'options': {
                        'temperature': self.temperature,
                        'num_predict': self.max_tokens
                    }
                },
                timeout=60.0
            )
            result = response.json()
        
        latency = (time.time() - start_time) * 1000
        content = result['message']['content']
        
        # Estimate tokens (Ollama doesn't return exact count)
        tokens = int(len(content.split()) * 1.3)
        
        return AgentResponse(
            content=content,
            tool_calls=[],  # No native tool calling
            tokens_used=tokens,
            cost=0.0,
            latency_ms=latency,
            provider="Ollama"
        )
    
    def get_cost_per_token(self) -> tuple[float, float]:
        return (0, 0)


# ============================================================================
# AGENT FACTORY
# ============================================================================

def create_agent(provider: str, config: dict) -> BaseAgent:
    """
    Factory function to create appropriate agent based on provider
    
    Args:
        provider: 'openai', 'anthropic', or 'ollama'
        config: Configuration dictionary
        
    Returns:
        Configured agent instance
    """
    providers = {
        'openai': OpenAIAgent,
        'anthropic': AnthropicAgent,
        'ollama': OllamaAgent
    }
    
    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(providers.keys())}")
    
    agent_class = providers[provider]
    return agent_class(config)


def load_agent_from_config(config_path: str = "config.yaml") -> BaseAgent:
    """
    Load agent configuration from YAML file and create agent
    
    Args:
        config_path: Path to config.yaml file
        
    Returns:
        Configured agent instance
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    provider = config['llm']['provider']
    agent_config = config['llm'][provider]
    agent_config['provider'] = provider
    
    logger.info(f"Loading {provider} agent with model {agent_config['model']}")
    
    return create_agent(provider, agent_config)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of LLM-agnostic framework"""
    
    # Option 1: Load from config file
    agent = load_agent_from_config("config.yaml")
    
    # Option 2: Create directly
    # agent = create_agent('openai', {
    #     'api_key': 'sk-...',
    #     'model': 'gpt-4-turbo',
    #     'temperature': 0.7,
    #     'max_tokens': 2000
    # })
    
    # Simple chat
    response = await agent.chat("What is Bitcoin?")
    print(f"Response: {response}")
    
    # Register a tool
    def get_price(symbol: str) -> float:
        """Get cryptocurrency price"""
        # Your implementation here
        return 50000.0
    
    price_tool = Tool(
        name="get_price",
        description="Get current cryptocurrency price in USD",
        function=get_price,
        parameters={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Crypto symbol (e.g., 'bitcoin')"}
            },
            "required": ["symbol"]
        }
    )
    
    agent.register_tool(price_tool)
    
    # Use with tools
    response = await agent.execute_with_tools("What's the price of Bitcoin?")
    print(f"Response: {response.content}")
    
    # Check usage stats
    stats = agent.get_stats()
    print(f"\nUsage Stats:")
    print(f"  Tokens: {stats['total_tokens']}")
    print(f"  Cost: ${stats['total_cost']:.4f}")
    print(f"  Provider: {stats['provider']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

