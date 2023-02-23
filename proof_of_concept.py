from __future__ import unicode_literals, print_function
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain

import whisper
import os
import pdb

from spacy.lang.en import English

from langchain import OpenAI, PromptTemplate, LLMChain
llm = OpenAI(temperature=0.3)

model = whisper.load_model("base")
result = model.transcribe("./sample_lecture.mp3")

lecture_text = result["text"]

nlp = English()
nlp.add_pipe(nlp.add_pipe('sentencizer')) 
doc = nlp(lecture_text)
texts = [sent.string.strip() for sent in doc.sents]


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



