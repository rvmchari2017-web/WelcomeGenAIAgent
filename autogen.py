from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import SourceMatchTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.tools import TeamTool
from autogen_agentchat.ui import Console
# from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
import nest_asyncio
# from google.colab import userdata
from dotenv import load_dotenv
import streamlit as st
import asyncio # Import asyncio
load_dotenv()
import os
nest_asyncio.apply()

# Define the async function to setup and run the agent team
async def setup_and_run_gemini_team(user_task: str, response_container) -> str:
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash-8b",
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    writer = AssistantAgent(name="writer", model_client=model_client, system_message="You are a helpful assistant.")
    reviewer = AssistantAgent(
        name="reviewer", model_client=model_client, system_message="You are a critical reviewer."
    )
    summarizer = AssistantAgent(
        name="summarizer",
        model_client=model_client,
        system_message="You combine the review and produce a revised response.",
    )
    team = RoundRobinGroupChat(
        [writer, reviewer, summarizer], termination_condition=SourceMatchTermination(sources=["summarizer"])
    )

    # Create a TeamTool that uses the team to run tasks, returning the last message as the result.
    tool = TeamTool(
        team=team, name="writing_team", description="A tool for writing tasks.", return_value_as_last_message=True
    )

    main_agent = AssistantAgent(
        name="main_agent",
        model_client=model_client,
        system_message="You are a helpful assistant that can use the writing tool.",
        tools=[tool],
    )

    full_response = ""
    async for chunk in main_agent.run_stream(task=user_task):
        try:
            full_response += chunk.text
        except Exception as e :
            print(f'error: {e}')
            full_response += str(chunk)
        finally:
            response_container.markdown(str(full_response))

    await model_client.close() # Close client after use
    return full_response


# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_prompt = st.chat_input("Ask for a story or say hi...")

if user_prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Create bot message container
    with st.chat_message("assistant"):
        response_container = st.empty()
        # Run async stream in Streamlit
        final_response = asyncio.run(setup_and_run_gemini_team(user_prompt, response_container))

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": final_response})