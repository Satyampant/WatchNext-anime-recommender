import sys
import os

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
        st.markdown("### 🎬 Recommended Anime:")
        st.write(response['recommendation_text'])
        
        # Display anime images and titles in a better layout
        if response['recommended_animes_with_images']:
            st.markdown("---")
            st.markdown("### 📺 Featured Anime:")
            
            for anime in response['recommended_animes_with_images']:
                # Create two columns: one for image, one for title
                col1, col2 = st.columns([1, 3])  # Image gets 1/4 width, title gets 3/4
                
                with col1:
                    st.image(anime['image_url'], width=150)
                
                with col2:
                    st.markdown(f"#### {anime['title']}")
                    st.write("")  # Add some spacing
                
                st.markdown("---")  # Divider between anime
        else:
            st.info("Could not retrieve specific anime source documents for display.")
    else:
        st.warning("No recommendations available. Please try a different query.")