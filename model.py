import openai
from llama_index import GPTSimpleKeywordTableIndex, SimpleDirectoryReader
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
import openai

def generate(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.4,
    max_tokens=600,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )

    return response.choices[0].text



def divide_array(arr, n):
    # Create an empty list to store the smaller arrays
    result = []
    
    # Iterate over the input array
    for i in range(0, len(arr), n):
        # Slice the input array into smaller arrays of length 'n'
        result.append(". ".join(arr[i:i+n]))
        
    # Return the list of smaller arrays
    return result


class Model:
    def __init__(self):
        self.llm = OpenAI(temperature=0.3)
        self.transcription = ""
        self.summary = ""
        self.docs = []
        self.summary_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        self.qa_chain = load_qa_chain(self.llm, chain_type="map_reduce")

        
    def setTranscription(self, audio):
        self.transcription = openai.Audio.transcribe("whisper-1", audio)["text"]

    def getTranscription(self):
        return self.transcription

    def createDocs(self):
        if(self.transcription == ""):
            return
        
        texts = self.transcription.split(". ")
        texts = divide_array(texts, 7)
        self.docs = [Document(page_content=t) for t in texts]
        return

    def setSummary(self):
        self.createDocs()
        self.summary = self.summary_chain.run(self.docs)

    def getSummary(self):
        return self.summary

    def answerQuestion(self, question):
        answer = self.qa_chain.run(input_documents=self.docs, question=question)
        return answer
    

    def getKeyTerms(self): # Work in Progress
        terms = {"term" : "definition"}
        return terms



# llm = OpenAI(temperature=0.3)
# file = open("example.mp3", "rb")
# transcription = openai.Audio.transcribe("whisper-1", file)["text"]

# print(transcription)

# texts = transcription.split(". ")
# texts = divide_array(texts, 7)

# docs = [Document(page_content=t) for t in texts]


# # Summarizing (TL:DR feature)
# chain = load_summarize_chain(llm, chain_type="map_reduce")
# print("Summary: ", chain.run(docs))

# # Question and Answering
# chain = load_qa_chain(llm, chain_type="map_reduce")
# query = "What is supabase?"
# print("Question:", query) 
# print("Answer:",chain.run(input_documents=docs, question=query))

