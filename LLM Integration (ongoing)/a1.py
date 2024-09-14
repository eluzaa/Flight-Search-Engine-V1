from typing import Dict, Any
import json
from langchain_openai import OpenAI
import autogen
from autogen.agentchat import UserProxyAgent, AssistantAgent
from flight_api import search_flights
import streamlit as st

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


config_list = [
    {
        "model": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
        "base_url": "http://192.168.78.1:1234/v1",
        "api_key": "lm-studio"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.2
}

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding", "use_docker": False},
)

flight_search_agent = AssistantAgent(
    name="FlightSearchAgent",
    llm_config=llm_config,
    system_message="You are a flight search specialist. "
)

def parse_llm_response(response: str) -> Dict[str, str]:
    lines = response.strip().split('\n')
    details = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            details[key.strip().strip('"')] = value.strip().strip(',').strip('"')
    return details

def process_flight_reservation(user_input: str):
    print("entered")
    user_proxy.initiate_chat(
        flight_search_agent,
        message=f"Analyze this flight request and provide search parameters in JSON format: {user_input}",
        max_turns=1
    )
    # user_proxy.send(flight_search_agent, "TERMINATE")
    # print("hello")
    flight_result = flight_search_agent.last_message()["content"]
    print("hello")
    print(flight_result)
    details = parse_llm_response(flight_result)
    search_params = json.dumps(details)
    print(type(details))
    # search_result = search_flights(search_params)
    search_result = search_flights(details)
    print("testing")
    # print(search_result)
    user_proxy.initiate_chat(
        flight_search_agent,
        message=f"Reformat this to be user presentable : {search_result}"
    )
    # user_proxy.send(flight_search_agent, "TERMINATE")
    presen = flight_search_agent.last_message()["content"]
    # print(presen)
    return presen

if __name__ == "__main__":
    user_input = \
    """You are a helpful assistant. Your goal is to find all the details of the user from the message he sends.
            The user input: {query}
            These details will be given to a function as parameters to get all the flights available.
            If time is not mentioned but duration of day is mentioned, enter time accordingly.

            Give the details in the below format.
            Source City Name: 
            Destination City Name: 
            Date: 
            Time: 
            Traveller Class:

            Get only the above details. Do not ask for any other details. If any detail in the above format is missing, leave it empty.
            Do not give any additional text. Give only the output needed in output format.
            """
    # result = process_flight_reservation(user_input)
    # print(json.dumps(result, indent=2))

    # user_proxy.send(flight_search_agent, "TERMINATE")
    st.title("Fly Smarter: Get Answers to All Your Flight Questions")
    question_input = st.text_area("Enter your query below.")
    if st.button("Submit"):
        result = process_flight_reservation(user_input.format(query=question_input))
        st.markdown(result)