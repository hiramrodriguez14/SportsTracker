from sentence_transformers import SentenceTransformer
from fragmentsDAO import FragmentDAO
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser


class ChatOllamabot:
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.max_turns = 5

    def chat(self, question, memory):
        
        instruction_to_system = """
       Do NOT answer the question. Given a chat history and the latest user question
       which might reference context in the chat history, formulate a standalone question
       which can be understood without the chat history. Do NOT answer the question under ANY circumstance ,
       just reformulate it if needed and otherwise return it as it is.
       
       Examples:
         1.History: "Human: Wgat is a beginner friendly exercise that targets biceps? AI: A begginer friendly exercise that targets biceps is Concentration Curls?"
           Question: "Human: What are the steps to perform this exercise?"

           Output: "What are the steps to perform the Concentration Curls exercise?"
           
         2.History: "Human: What is the category of bench press? AI: The category of bench press is strength."
           Question: "Human: What are the steps to perform the child pose exercise?"
           
           Output: "What are the steps to perform the child pose exercise?"
       """
       
        llm = ChatOllama(model="llama3.2", temperature=0)
        
        question_maker_prompt = ChatPromptTemplate.from_messages(
          [
            ("system", instruction_to_system),
             MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"), 
          ]
        )
       
        question_chain = question_maker_prompt | llm | StrOutputParser()
       
        newQuestion = question_chain.invoke({"question": question, "chat_history": memory})
          
        actual_question = self.contextualized_question(memory, newQuestion, question)
        
        emb = self.model.encode(actual_question)  
        

        dao = FragmentDAO()
        fragments = dao.getFragments(str(emb.tolist()))
        context = [f[3] for f in fragments]

        
        for f in fragments:
            context.append(f[3])
            
        documents = "\n\n---\n\n".join(c for c in context) 


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
            "question": actual_question,
            "documents": documents,
        })
        
       # Keep only the last N turns (each turn = 2 messages)
        if len(memory) > 2 * self.max_turns:
            memory = memory[-2 * self.max_turns:]


        # Add new interaction as direct messages
        memory.append( HumanMessage(content=actual_question))
        memory.append( AIMessage(content=answer))

        
       
        print(newQuestion + " -> " + answer)
            
        for interactions in memory:
           print(interactions)
           print() 

        return answer, memory
    
    def contextualized_question(self, chat_history, new_question, question):
        if chat_history:
            return new_question
        else:
            return question
