from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
import os

from langchain import OpenAI, PromptTemplate, LLMChain
llm = OpenAI(temperature=0.3)

text_splitter = CharacterTextSplitter()

txt_dir = 'lecture_transcription.txt'

with open(txt_dir) as f:
    data = f.read()

texts = data.splitlines()


docs = [Document(page_content=t) for t in texts]

# Summarizing (TL:DR feature)
chain = load_summarize_chain(llm, chain_type="map_reduce")
print("Summary: ", chain.run(docs))

# Lecture Key Points


# Question and Answering
chain = load_qa_chain(llm, chain_type="refine")
query = "What aspect of West Africa languages such as Twi makes it possible for certain drums?"
print("Question: ", query) 
print(chain.run(input_documents=docs, question=query))

