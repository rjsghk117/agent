from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

def get_weather(city:str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}"

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "부산의 날씨는 어때?"}]}
)

# print(result["messages"][-1].content_blocks)
# [{'type': 'text', 'text': '부산은 현재 항상 맑은 날씨라고 합니다. ☀️'}]

# print(result)
# {'messages': [HumanMessage(content='부산의 날씨는 어때?', additional_kwargs={}, response_metadata={}, id='ca21cece-6341-4114-a5fd-6e8de8aa4148'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 18, 'prompt_tokens': 144, 'total_tokens': 162, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-5.5-2026-04-23', 'system_fingerprint': None, 'id': 'chatcmpl-EVpJRK3ZzRUcHgqcm784nkh2z3Ai5', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a10f10-ca18-7563-900e-93db844a0099-0', tool_calls=[{'name': 'get_weather', 'args': {'city': '부산'}, 'id': 'call_H4YlU9REk2ov7fjcOzbjmuws', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 144, 'output_tokens': 18, 'total_tokens': 162, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), ToolMessage(content="It's always sunny in 부산", name='get_weather', id='5d2ed5ee-9c98-474f-8e9e-b71db4d1a580', tool_call_id='call_H4YlU9REk2ov7fjcOzbjmuws'), AIMessage(content='부산의 날씨는 맑습니다. ☀️', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 16, 'prompt_tokens': 178, 'total_tokens': 194, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-5.5-2026-04-23', 'system_fingerprint': None, 'id': 'chatcmpl-EVpJTt6y0tZsdPckoBCrWwj9C79ZM', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--01a10f10-d03b-70b2-8967-934c8f4df360-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 178, 'output_tokens': 16, 'total_tokens': 194, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}

print(result["messages"][-1].content)
# 부산의 날씨는 맑습니다. ☀️