import streamlit as st
from textwrap import dedent
import openai
from duckduckgo_search import DDGS

# Set up the Streamlit app
st.title("AI Personal Finance Planner 💰")
st.caption("Manage your finances with AI Personal Finance Manager by creating personalized budgets, investment plans, and savings strategies using GPT-4")

# Get OpenAI API key from user
openai_api_key = st.text_input("Enter OpenAI API Key to access GPT-4", type="password")

if openai_api_key:
    openai.api_key = openai_api_key

    def get_search_terms(goals, situation):
        messages = [
            {
                "role": "system",
                "content": "You are a world-class financial researcher."
            },
            {
                "role": "user",
                "content": f"Given a user's financial goals and current financial situation, generate a list of 3 search terms for finding relevant financial advice, investment opportunities, and savings strategies.\n\nUser's financial goals: {goals}\nUser's current financial situation: {situation}\n\nList the 3 search terms:"
            }
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages
        )
        search_terms = response['choices'][0]['message']['content'].strip()
        return search_terms.split('\n')

    def get_search_results(search_terms):
        search_results = []
        ddgs = DDGS()
        for term in search_terms:
            results = ddgs.text(term, max_results=3)
            for result in results:
                search_results.append(result['title'] + ": " + result['href'])
        return "\n".join(search_results)

    def get_financial_plan(goals, situation, search_results):
        messages = [
            {
                "role": "system",
                "content": "You are a senior financial planner."
            },
            {
                "role": "user",
                "content": f"Given a user's financial goals, current financial situation, and a list of research results, your goal is to generate a personalized financial plan that meets the user's needs and preferences.\n\nUser's financial goals: {goals}\nUser's current financial situation: {situation}\nResearch results: {search_results}\n\nGenerate a personalized financial plan that includes suggested budgets, investment plans, and savings strategies. Ensure the plan is well-structured, informative, and engaging. Ensure you provide a nuanced and balanced plan, quoting facts where possible. Focus on clarity, coherence, and overall quality."
            }
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        return response['choices'][0]['message']['content'].strip()

    # Input fields for the user's financial goals and current financial situation
    financial_goals = st.text_input("What are your financial goals?")
    current_situation = st.text_area("Describe your current financial situation")

    if st.button("Generate Financial Plan"):
        with st.spinner("Processing..."):
            search_terms = get_search_terms(financial_goals, current_situation)
            search_results = get_search_results(search_terms)
            response = get_financial_plan(financial_goals, current_situation, search_results)
            st.write(response)
