import sys
import os

current_dir = os.path.dirname(__file__)

project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

# --- Configuration ---
st.set_page_config(page_title="Anime Recommender", layout="wide")

load_dotenv()

# --- Pipeline Initialization (Cached) ---
@st.cache_resource
def init_pipeline():
    """Initializes and caches the heavy-duty recommendation pipeline."""
    # Assuming AnimeRecommendationPipeline correctly initializes the LLM and retriever
    return AnimeRecommendationPipeline()

pipeline = init_pipeline()

# --- Streamlit UI ---
st.title("🎬 Anime Recommender System")
st.markdown("Enter your anime preferences below, and the system will provide tailored recommendations.")

query = st.text_input(
    "Enter your anime preferences (e.g., light-hearted anime with school settings):",
    placeholder="Adventure, fantasy anime with great world-building"
)

if query:
    with st.spinner("Fetching recommendations for you..."):
        # The recommend method is assumed to return the structured dictionary:
        # { "recommendation_text": str, "recommended_animes_with_images": list }
        try:
            response = pipeline.recommend(query)
        except Exception as e:
            st.error(f"An error occurred while generating recommendations: {e}")
            response = None

    if response:
        st.markdown("---")
        
        # 1. Display the overall recommendation text from the LLM
        st.markdown("### 💬 Your Personalized Recommendation Summary")
        st.info(response['recommendation_text'])

        # 2. Display the individual recommended animes with images
        st.markdown("### 🖼️ Recommended Anime Titles")
        st.write(response)
        
        animes = response.get('recommended_animes_with_images', [])

        if not animes:
            st.warning("Could not retrieve specific anime source documents for display.")
        
        # Display recommendations in a grid format (2 columns per row)
        cols = st.columns(2)
        
        for i, anime in enumerate(animes):
            title = anime.get('title', 'Unknown Title')
            image_url = anime.get('image_url')

            # Use the modulo operator to distribute items into columns
            col = cols[i % 2]
            
            with col:
                st.markdown(f"**{i+1}. {title}**", unsafe_allow_html=True)
                
                # Use Streamlit columns within the main column for image and details
                img_col, text_col = st.columns([1, 2])
                
                with img_col:
                    if image_url:
                        # Display the image using the provided URL
                        st.image(
                            image_url, 
                            caption=title, 
                            use_column_width="auto"
                        )
                    else:
                        st.markdown("*(Image not available)*")

                with text_col:
                    
                    st.markdown(f"**Title:** {title}")
                    st.markdown(f"**Source Document:** Retrieved as a top match to your query.")
                    st.markdown("---")