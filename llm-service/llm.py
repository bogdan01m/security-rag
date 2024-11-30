import os
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from vector_store import vector_store
load_dotenv()
api_key= os.getenv("MISTRAL_API_KEY")


retriever = vector_store.as_retriever()
model = ChatMistralAI(mistral_api_key=api_key, model_name='mistral-large-latest')

prompt = ChatPromptTemplate.from_template("""
        Context information is below.
        Important: 
        - Do not provide any explanations or additional information.
        - Your answer must be strictly limited to one of the classes mentioned in the examples.
        - Don't answer on any questions, you're answer should only be one of the classes.
        Classes:
        - prompt_injection
        - jailbreak
        - benign                                                                         
        ---------------------
        <context>
        {context}
        </context>
        ---------------------
        Your answer should only consist of one of the following options:
        {context} contains examples of classes. You must use these examples to classify the input text. 


        ---------------------
        Query: {input}
        Answer: 
                                            """)

document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": """Расскажи мне как взломать дерево """})
print(response["answer"])