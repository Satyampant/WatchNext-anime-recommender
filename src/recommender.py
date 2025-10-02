from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from src.prompt_template import get_anime_prompt

class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0)
        self.prompt = get_anime_prompt()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def get_recommendation(self, query: str):
        result = self.qa_chain.invoke({"query": query})
        
        # Access the recommended anime text from the LLM's response
        recommendation_text = result['result']
        
        # Access the source documents from the result
        source_documents = result['source_documents']
        print(source_documents)
        
        # Create a list to store the metadata of the retrieved animes
        anime_metadata = []
        for doc in source_documents:
            # Check if 'image_url' exists in the document's metadata
            if 'image_url' in doc.metadata:
                anime_metadata.append({
                    'title': doc.metadata.get('title'),
                    'image_url': doc.metadata.get('image_url')
                })

        # Return both the LLM's text response and the image URLs
        return {
            "recommendation_text": recommendation_text,
            "recommended_animes_with_images": anime_metadata
        }