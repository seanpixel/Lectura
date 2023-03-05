import openai
import re
import spacy

# import en_core_web_sm

# nlp = en_core_web_sm.load()
nlp = spacy.load('en_core_web_sm')
openai.api_key = "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"

# Split article into sentences
def split_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    sentences = re.split(r'(?<=[^A-Z].[.!?])\s+(?=[A-Z])', text)
    
    return sentences

# Group sentences (n is # of sentences)
def group_sentences(arr, n):
    result = []
    
    for i in range(0, len(arr), n):
        result.append(". ".join(arr[i:i+n]))
        
    return result

def generate(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text

# summarization function
def summarize_text(text):
    chunks = split_sentences(text)
    chunks = group_sentences(chunks, 30)
    

    bulletpoints = "Nothing here yet"

    for i in range(0, len(chunks)):
        chunk = chunks[i]
        prompt = f'''I am trying to make a study guide based on a lecture.\n\nHere is the lecture so far summarized in bulletpoints:\n{bulletpoints}\n\nSummarize the next part of the lecture in the form of bulletpoints so that the study guide flows.\n\nNext part of the lecture in Bulletpoints:\n{chunk}'''
        
        # Remove Placeholder
        if i == 0:
            bulletpoints = ""

        summary = generate(prompt).strip()
        bulletpoints += summary
        print(str(i) + "/" + str(len(chunks)))

    return bulletpoints


# in_file_name = "example.txt"
# out_file_name = "summary.txt"

# file = open(in_file_name)
# text = file.read()
# summary = summarize_text(text)

# answer_file = open(out_file_name, 'w')
# answer_file.write(summary)
