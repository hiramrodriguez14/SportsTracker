from sentence_transformers import SentenceTransformer
from app.model.dao.fragmentsDAO import FragmentDAO
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain.schema.output_parser import StrOutputParser
from app.model.dao.docsDAO import DocumentDAO


class ChatOllamabot:
    def __init__(self):
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.max_turns = 5

    def chat(self, question, memory):
        
        instruction_to_system = """
       You are an AI assistant that enhances the last human question.Given a chat history and the latest user question at the end
       which might reference context in the chat history, your task is to check if the question depends on the chat history, if thats true add context to the question so it can be understood without history. Otherwise just return the question as it is. You should always return a question.  
       Do NOT answer the question under ANY circumstance and if the user mentions an exercise do not change the name of it.
       
       Examples:
         1.History: "Human: What is a beginner friendly exercise that targets biceps? AI: A begginer friendly exercise that targets biceps is Concentration Curls?"
           Question: "Human: What are the steps to perform this exercise?"

           Output: "What are the steps to perform the Concentration Curls exercise?"
           
         2.History: "Human: What is the category of bench press? AI: The category of bench press is strength."
           Question: "Human: What are the steps to perform the child pose exercise?"
           
           Output: "What are the steps to perform the child pose exercise?"
           
        3.History: "Human: What is the category of bench press? AI: The category of bench press is strength."
           Question: "Human: What is the level of the exercise?"
           
           Output: "What is the level of the bench press exercise?"
           
        4.History: "Human: What is a back exercise for beginners? AI: A good one is the resistance band row."
          Question: "Human: What are some other back exercises for beginners?"
          
          Output: "What are some other back exercises for beginners?"


        5.History: "Human: What equipment do I need for squats? AI: You can use a barbell, dumbbells, or just your bodyweight."
            Question: "Human: What are the benefits of squats?"
            
            Output: "What are the benefits of squats?"

           
       """
       
        llm1 = ChatOllama(model="granite3.3:2b", temperature=0)
        
        question_maker_prompt = ChatPromptTemplate.from_messages(
          [
            ("system", instruction_to_system),
             MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"), 
          ]
        )
       
        question_chain = question_maker_prompt | llm1 | StrOutputParser()
       
        newQuestion = question_chain.invoke({"question": question, "chat_history": memory})
          
        actual_question = self.contextualized_question(memory, newQuestion, question)
        
        emb = self.model.encode(actual_question)  
        

        fragment_dao = FragmentDAO()
        
       
        
        doc_dao = DocumentDAO()
        
      

        doc_ids = fragment_dao.getFragments(str(emb.tolist()))
        
        print(doc_ids)

        doc_map = doc_dao.getDocuments(doc_ids)
        
        print(doc_map)

        docnames = [doc_map[did] for did in doc_ids if did in doc_map]

        seen = set()
        context = []
        for doc in docnames:
         if doc["docname"] not in seen:
             context.append(doc["content"])
             seen.add(doc["docname"])
             
        

        print("context: " + str(context))
        documents = "\n\n---\n\n".join(context)



        prompt = PromptTemplate(
            template="""You are an assistant for exercise question answering tasks. Use only the following documents to answer the question;each document has the name of the exercise, the force, level, mechanic, equipment, primary and secondary muscles, and the steps to perform the exercise. If you dont know the answers, just say that you dont know. Use five sentences maximum (a list of instructions count as 1 sentence), keep the answer concise and make sure to answer the full question:
                        
            Documents: {documents}
            Question: {question}        

            Answer:""",
            input_variables=["documents", "question"],
        )

        llm2 = ChatOllama(model="llama3.2", temperature=0)
        rag_chain = prompt | llm2 | StrOutputParser()

        answer = rag_chain.invoke({
            "question": actual_question,
            "documents": documents,
        })
        
        if len(memory) > 2 * self.max_turns:
            memory = memory[-2 * self.max_turns:]

        memory.append("human: " + actual_question)
        memory.append("AI: " + answer)

        print("User question: " + question)
        print("First LLM response: " + newQuestion )
        print("Second LLM response: " + answer)
        print("Context: " + documents)


        return answer, memory, documents
    
    def contextualized_question(self, chat_history, new_question, question):
        if chat_history:
            return new_question
        else:
            return question
