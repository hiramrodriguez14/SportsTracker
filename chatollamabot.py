from sentence_transformers import SentenceTransformer
from fragmentsDAO import FragmentDAO
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser


class ChatOllamabot:
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.max_turns = 5

    def chat(self, question, memory):
        
       
        
        question_maker_prompt = PromptTemplate(
          template="""
      Given a chat history and the latest user question, return ONLY the reformulated question if context is needed.

Do not explain.
Do not include code.
Do not add labels like "Reformulated Question:".
Do not answer the question.

Examples:
---
Question: What muscles does this exercise work?
History: User: What is a bench press? Assistant: It targets the chest.
Output: What muscles does a bench press work?
---

Question: How many sets for this?
History: User: What is a deadlift? Assistant: Its for the back.
Output: How many sets for a deadlift?
---

Question: {question}
History: {history}
Output:""",
        input_variables=["question", "history"],
        )
        
        llm = ChatOllama(model="llama3.2", temperature=0)
        
        question_chain = question_maker_prompt | llm | StrOutputParser()
        
        newQuestion = question_chain.invoke({
            "question": question,
            "history": memory
        })
    
        
       
        emb = self.model.encode(newQuestion)  
        

        dao = FragmentDAO()
        fragments = dao.getFragments(str(emb.tolist()))
        context = [f[3] for f in fragments]

        
        for f in fragments:
            context.append(f[3])
            
        documents = "\n\n---\n\n".join(c for c in context) #Si algo falla revisar esto


        prompt = PromptTemplate(
            template="""You are an assistant for question answering tasks. Use the following documents to answer the question.
            If you dont know the answers, just say that you dont know. Use five sentences maximum and keep the answer concise:
            
            Documents: {documents}
            Question: {question}        

            Answer:""",
            input_variables=["documents", "question"],
        )

        llm = ChatOllama(model="llama3.2", temperature=0)
        rag_chain = prompt | llm | StrOutputParser()

        answer = rag_chain.invoke({
            "question": newQuestion,
            "documents": documents,
        })
        
         # Keep only the last 2
        if len(memory) > self.max_turns:
            del memory[0]

        # Add new interaction
        interaction = f"User: {newQuestion}\nAssistant: {answer}"
            
        memory.append(interaction)
        
       
        print(newQuestion + " -> " + answer)
            
        for interactions in memory:
           print(interactions)
           print()  # opcional: línea en blanco entre interacciones


        return answer, memory
