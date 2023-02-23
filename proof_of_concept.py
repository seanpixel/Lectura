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
nlp.add_pipe(nlp.create_pipe('sentencizer')) # updated
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



# queries = ["What aspect of West Africa languages such as Twi makes it possible for certain drums, like the atumpan, to literally speak? How are spoken and drum speech related?", "How is the term polyvocality applied in this chapter?", "Who Ladysmith Black Mambazo and what did they contribute to South African musical and socio-political history?", "How has the jeliya tradition been significant in the history of Mande society and culture?", "What cultures and music traditions of the African diaspora were mentioned in this chapter?", "Traditionally, what was the function of the Fontomfrom ensemble and its music in Akan societies? Has modernization changed this? if so, how?", "What were the six musical Africanisms listed in the chapter? How do they apply in the various musical examples explored?"]

# for query in queries:
#     print(chain.run(input_documents=docs, question=query))

