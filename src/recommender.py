from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0)
        self.prompt = get_anime_prompt()
        
        # Store retriever as instance variable
        self.retriever = retriever
        
        # Debug: Test if retriever works before creating chain
        print(f"\n=== Testing retriever before chain creation ===")
        test_docs = retriever.invoke("anime")  # Use invoke instead of get_relevant_documents
        print(f"Retriever test returned {len(test_docs)} documents")
        if test_docs:
            print(f"Sample doc metadata: {test_docs[0].metadata}")

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def get_recommendation(self, query: str):
        result = self.qa_chain.invoke({"query": query})
        
        recommendation_text = result['result']
        source_documents = result.get('source_documents', [])
        
        print(f"=== Source documents from chain: {len(source_documents)} ===")
        
        # Use the instance retriever directly
        if not source_documents:
            print("=== Using instance retriever ===")
            source_documents = self.retriever.invoke(query)
            print(f"=== Instance retriever got {len(source_documents)} documents ===")
        
        anime_metadata = []
        for doc in source_documents:
            print(f"Doc metadata: {doc.metadata}")
            if 'image_url' in doc.metadata:
                anime_metadata.append({
                    'title': doc.metadata.get('title'),
                    'image_url': doc.metadata.get('image_url')
                })

        return {
            "recommendation_text": recommendation_text,
            "recommended_animes_with_images": anime_metadata
        }