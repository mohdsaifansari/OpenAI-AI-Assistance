from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st
import pandas as pd

openai.api_key = "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"
model = SentenceTransformer('all-MiniLM-L6-v2')

import os
from pinecone import Pinecone, ServerlessSpec

#pc = Pinecone(api_key='518db704-265b-41a8-89df-e7c0b2453317', environment='gcp-starter')
pc = Pinecone(api_key='518db704-265b-41a8-89df-e7c0b2453317', environment='gcp-starter')
index = pc.Index("ai-assitance")

def load_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df
# Now do stuff
#if 'ai-assitance' not in pc.list_indexes().names():
#   pc.create_index(
#       name='ai-assitance',
#       dimension=384,
#       metric='cosine',
#       spec=ServerlessSpec(
#           cloud='gcp',
#           region='us-central1'
#       )
#   )

#def find_match(input):
#    input_em = model.encode(input).tolist()
#    result = index.query(input_em, top_k=2, includeMetadata=True)
#    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']
def answer_question_from_csv(df, question):
    # Example logic: Search for the question in the DataFrame and return the corresponding answer
    # This logic can be customized based on your specific use case and the structure of your DataFrame
    answer = "No answer found"
    if question in df.columns:
        answer = df[question].iloc[0]  # Assuming the question corresponds to a column in the DataFrame
    return answer
def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(vector=input_em, top_k=2, includeMetadata=True)
    if 'matches' in result and len(result['matches']) >= 2:
        return result['matches'][0]['metadata']['text'] + "\n" + result['matches'][1]['metadata']['text']
    else:
        return "No matches found"


def query_refiner(conversation, query):
    prompt = "Explain the concept of infinite universe to a 5th grader in a few sentences"

    OPENAI_MODEL = "gpt-3.5-turbo-instruct"
    DEFAULT_TEMPERATURE = 1
    
    response = openai.completions.create(
        model=OPENAI_MODEL,
        prompt=prompt,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=1000,
        n=1,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0.1,
    ) 

    # Check if the response was successful
    if response and response.choices:
        refined_query = response.choices[0].text
        return refined_query
    else:
        return "Error: Unable to refine the query"


    prompt = "Explain the concept of infinite universe to a 5th grader in a few sentences"

    OPENA_AI_MODEL = "gpt-3.5-turbo-instruct"
    DEFAULT_TEMPERATURE = 1
    
    response = openai.completions.create(
    model=OPENA_AI_MODEL,
    prompt=prompt,
    temperature=DEFAULT_TEMPERATURE,
    max_tokens=500,
    n=1,
    stop=None,
    presence_penalty=0,
    frequency_penalty=0.1,
    ) 
   # response = openai.completions.create(
   # model="gpt-3.5-turbo-instruct",
   # prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
   # temperature=0.7
   # )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string

