import logging
from typing import Any, Dict, List

from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import LLMChain, RetrievalQA, RetrievalQAWithSourcesChain

# from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI  # Updated import
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS

from corpus import Corpus

logging_level = logging.INFO
logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging_level)
logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(self, llm_context: Dict[str, Any]):
        self.llm_context = llm_context
        self.corpus = None  # TODO return get_count => corpus.get_count

    def get_documents_count(self):
        return self.corpus.get_count() if self.corpus else 0

    def initialize_search(self):
        llm = AzureChatOpenAI(
            openai_api_type=self.llm_context["openai_api_type"],
            openai_api_base=self.llm_context["openai_api_base"],
            openai_api_version=self.llm_context["openai_api_version"],
            deployment_name=self.llm_context["deployment_name"],
            openai_api_key=self.llm_context["openai_api_key"],
            temperature=self.llm_context["chat_model_temperature"],
        )

        # conversational memory
        conversational_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=1,  # use conversational modelbecause it is less exeennsive, not for dialog
            return_messages=True,
        )

        # configure retriver
        k = self.llm_context["retriever_k"]
        score_threshold = self.llm_context["retriever_score_threshold"]
        search_type = self.llm_context["retriever_search"]
        # similarity_score_threshold
        # similarity
        # mmr
        retriever = self.vector_store.as_retriever(
            search_type=search_type, search_kwargs={"k": k, "score_threshold": score_threshold}
        )
        self.retriever = retriever

        # retrieval qa chain
        # can add a prompt here as kwags
        # chain_type_kwargs = {"verbose": True, "combine_prompt": COMBINE_PROMPT, "question_prompt": QUESTION_PROMPT}

        question_prompt_template = """Use the following portion of a long document to see if any of the text is relevant to answer the question. 
        Return any relevant text verbatim.
        ---
        {context}
        ---
        Question: {question}
        Relevant text, if any:"""

        QUESTION_PROMPT = PromptTemplate(template=question_prompt_template, input_variables=["context", "question"])

        combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.
        QUESTION: Which state/country's law governs the interpretation of the contract?
        =========
        Content: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
        Source: 28-pl
        Content: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.\n\n11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.\n\n11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.\n\n11.9 No Third-Party Beneficiaries.
        Source: 30-pl
        Content: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
        Source: 4-pl
        =========
        FINAL ANSWER: This Agreement is governed by English law.
        SOURCES: 28-pl
        QUESTION: What did the president say about Michael Jackson?
        =========
        Content: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia's Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
        Source: 0-pl
        Content: And we won't stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet's use this moment to reset. Let's stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet's stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can't change how divided we've been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who'd grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
        Source: 24-pl
        Content: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I've always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I'm taking robust action to make sure the pain of our sanctions  is targeted at Russia's economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what's happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
        Source: 5-pl
        Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt's based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer's, diabetes, and more. \n\nA unity agenda for the nation. \n\nWe can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. \n\nIn this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. \n\nWe have fought for freedom, expanded liberty, defeated totalitarianism and terror. \n\nAnd built the strongest, freest, and most prosperous nation the world has ever known. \n\nNow is the hour. \n\nOur moment of responsibility. \n\nOur test of resolve and conscience, of history itself. \n\nIt is in this moment that our character is formed. Our purpose is found. Our future is forged. \n\nWell I know this nation.
        Source: 34-pl
        =========
        FINAL ANSWER: The president did not mention Michael Jackson.
        SOURCES:  
        QUESTION: {question}
        =========
        {summaries}
        =========
        FINAL ANSWER:"""
        # COMBINE_PROMPT = PromptTemplate(
        #    template=combine_prompt_template,
        #    input_variables=["summaries", "question", "source"]
        # )

        summary_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.
        {context}
        Question: {question}
        Relevant text, if any:"""

        SUMMARY_PROMPT = PromptTemplate(template=question_prompt_template, input_variables=["context", "question"])

        chain_type_kwargs = {
            "verbose": True,
            #                     "combine_prompt": COMBINE_PROMPT,
            #  "question_prompt": QUESTION_PROMPT}
            "prompt": QUESTION_PROMPT,
        }

        # create a chainqa = RetrievalQAWithSourcesChain.from_chain_type(
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # "map_reduce",  #
            retriever=retriever,
            # combine_documents_chain = LLMChain(llm=llm, primpt=SUMMARY_PROMPT),
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
        )
        # logger.info(qa({"question": "How do i deploy chains?", "verbose": True}, return_only_outputs=False))
        self.chain = qa_chain

        # LLM chain consisting of the LLM and a prompt
        agent_prompt_template = """Given the following extracted parts of a candidates resumes and a question, create a final answer with references ("SOURCES"). 
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.
        {context}
        Question: {question}
        Relevant text, if any:"""
        AGENT_PROMPT = PromptTemplate(template=question_prompt_template, input_variables=["context", "question"])

        llm_chain = LLMChain(llm=llm, prompt=AGENT_PROMPT)

        # wrap qa as a tool
        tools = [
            Tool(
                name="Knowledge Base",
                # func=qa.run,
                # func=qa_chain,  # obly for QARetrievalWith Sources
                func=qa_chain.run,
                # func=lambda q: qa_chain(q, return_only_outputs=False), #Note the lambda
                description=("use this tool to find relevant resumes of candidates matching a question."),
            ),
            Tool(
                name="Resume Search",
                # func=qa.run,
                # func=qa,  # obly for QARetrievalWith Sources
                # func=llm_chain.run,
                func=lambda question, context: llm_chain.run(
                    {"question": question, "context": context}, return_only_outputs=False
                ),  # Note the lambda
                description=("use this tool when evaluating best candidates based on porvided resumes."),
            ),
        ]

        # create an agent

        agent = initialize_agent(
            # agent='chat-conversational-react-description',
            # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # allow tools with multipke parameters
            tools=tools,
            llm=llm,
            verbose=self.llm_context["verbose"],
            max_iterations=3,
            early_stopping_method="generate",
            memory=conversational_memory,
        )

        self.agent = agent

        # run
        # agent(query)

    def initialize_with_uploaded_documents(self, pdf_docs):
        self.corpus = Corpus(llm_context=self.llm_context)
        self.vector_store = self.upload_to_vector_store(pdf_docs)

    def upload_to_vector_store(self, pdf_docs):
        # upload from a list of UploadFiles
        # upload a ocuments into a vector store
        logger.info(f"Processing {len(pdf_docs)} document(s)...")
        if pdf_docs:
            documents = self.corpus.load_documents(pdf_docs)
            if documents:
                text_chunks = self.corpus.split_documents(
                    documents,
                    chunk_size=self.llm_context["embedding_chunk_size"],
                    chunk_overlap=self.llm_context["embedding_chunk_overlap"],
                )
                vector_store = self.corpus.build_vector_store(text_chunks)

                count = len(pdf_docs)
                logger.info(f"Indexed {count} document(s)")

            else:
                logger.info("Something went wrong")
        return vector_store


# sequentiql vchain
# https://python.langchain.com/docs/modules/chains/foundational/sequential_chains

'''
from langchain import FewShotPromptTemplate

# create our examples
examples = [
    {
        "query": "How are you?",
        "answer": "I can't complain but sometimes I still do."
    }, {
        "query": "What time is it?",
        "answer": "It's time to get a watch."
    }
]

# create a example template
example_template = """
User: {query}
AI: {answer}
"""

# create a prompt example from above template
example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

# now break our previous prompt into a prefix and suffix
# the prefix is our instructions
prefix = """The following are exerpts from conversations with an AI
assistant. The assistant is typically sarcastic and witty, producing
creative  and funny responses to the users questions. Here are some
examples: 
"""
# and the suffix our user input and output indicator
suffix = """
User: {query}
AI: """

# now create the few shot prompt template
few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n"
)
'''
