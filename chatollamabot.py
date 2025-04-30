from sentence_transformers import SentenceTransformer
from fragmentsDAO import FragmentDAO
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser


class ChatOllamabot:
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")
        
    def chat(self, question):
        emb = self.model.encode(question)
        
        dao = FragmentDAO()
        
        fragments = dao.getFragments(str(emb.tolist()))
        
        context = []
        
        for f in fragments:
            context.append(f[3])
            
        documents = "\n\n---\n\n".join(c for c in context) #Si algo falla revisar esto
        
        prompt = PromptTemplate(
            template = """You are an assistant for question answering tasks. Use the following documents to answer the question.
            If you dont know the answers, just say that you dont know. Use five sentences maximum and keep the answer concise:
            Documents: {documents}
            Question: {question}
            Answer:
            """,
            input_variables = ["question", "documents"],
        )
        
        print(prompt)
        print(prompt.format(question = question, documents = documents))
        
        llm = ChatOllama(
            model = "llama3.2",
            temperature = 0
        )
        
        #Create a chain combining the prompt template and LLM
        rag_chain = prompt | llm | StrOutputParser()
        
        #Question
        
        answer = rag_chain.invoke({"question": question, "documents": documents})
        print(answer)
        return answer
