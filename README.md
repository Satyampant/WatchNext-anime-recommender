# 🎬 Anime Recommender System

An intelligent anime recommendation system built with RAG (Retrieval-Augmented Generation) that provides personalized anime suggestions based on user preferences.

## 🌟 Features

- **Intelligent Recommendations**: Uses RAG with LLM to provide contextually relevant anime suggestions
- **Vector Search**: Leverages ChromaDB for efficient semantic search across anime database
- **Interactive UI**: Clean Streamlit interface with anime images and details
- **Personalized Results**: Analyzes user preferences to match with suitable anime titles

## 🏗️ Architecture

```
User Query → Vector Store (ChromaDB) → Retriever → LLM (Groq) → Recommendations
```

The system uses:
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` for text vectorization
- **Vector Store**: ChromaDB for similarity search
- **LLM**: Groq API with Llama model for generating recommendations
- **Framework**: LangChain for RAG pipeline orchestration

## 📁 Project Structure

```
anime-recommender/
├── app/
│   ├── __init__.py
│   └── app.py                 # Streamlit UI
├── pipeline/
│   ├── __init__.py
│   ├── build_pipeline.py      # Vector store builder
│   └── pipeline.py            # Main recommendation pipeline
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Data processing
│   ├── vector_store.py        # ChromaDB operations
│   ├── recommender.py         # RAG recommendation logic
│   └── prompt_template.py     # LLM prompt templates
├── utils/
│   ├── __init__.py
│   ├── logger.py              # Logging configuration
│   └── custom_exception.py    # Custom exceptions
├── config/
│   └── config.py              # Configuration settings
├── data/
│   ├── anime_with_synopsis.csv    # Original dataset
│   └── anime_updated.csv          # Processed dataset
├── chroma_db/                 # Vector store (generated)
├── logs/                      # Application logs
├── pyproject.toml             # Project dependencies
├── Dockerfile                 # Docker configuration
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- uv (recommended) or pip
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd anime-recommender
   ```

2. **Install dependencies using uv**
   ```bash
   uv pip install -e .
   ```
   
   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   MODEL_NAME=llama-3.3-70b-versatile
   ```

4. **Build the vector store**
   ```bash
   python pipeline/build_pipeline.py
   ```
   This will:
   - Load and process the anime dataset
   - Create embeddings
   - Build and persist the ChromaDB vector store

5. **Run the application**
   ```bash
   streamlit run app/app.py
   ```
   
   The app will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### Build the Docker image

```bash
docker build -t anime-recommender .
```

### Run the container

```bash
docker run -p 8501:8501 --env-file .env anime-recommender
```

Or with inline environment variables:

```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_api_key \
  -e MODEL_NAME=llama-3.3-70b-versatile \
  anime-recommender
```

Access the app at `http://localhost:8501`

## 📊 Dataset

The system uses an anime dataset with the following fields:
- **English name**: Anime title
- **Genres**: Anime genres
- **Synopsis**: Plot description
- **Image URL**: Anime poster/cover image

Dataset is processed to filter out entries with "Unknown" titles and combine information into searchable text.

## 🛠️ Usage

1. Open the Streamlit app in your browser
2. Enter your anime preferences in the text box (e.g., "action anime with great character development")
3. The system will:
   - Search the vector database for relevant anime
   - Generate personalized recommendations using the LLM
   - Display 3 anime titles with images and descriptions

### Example Queries

- "Light-hearted anime with school settings"
- "Dark fantasy anime with complex storylines"
- "Sports anime with character growth"
- "Slice of life anime about friendship"

## 🔧 Configuration

Edit `config/config.py` to customize:
- API keys
- Model names
- Vector store settings
- Retrieval parameters

## 📝 Logging

Logs are stored in the `logs/` directory with daily rotation:
- Format: `log_YYYY-MM-DD.log`
- Includes timestamps, log levels, and detailed error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License.

## 👤 Author

**Satyam**
- Email: satyampant420@example.com

## 🙏 Acknowledgments

- LangChain for RAG framework
- Groq for LLM API
- HuggingFace for embeddings
- ChromaDB for vector storage
- Streamlit for the UI framework

## 🐛 Troubleshooting

### Vector store is empty
Run `python pipeline/build_pipeline.py` to build the vector store before starting the app.

### Import errors
Make sure you've installed the project in editable mode: `uv pip install -e .`

### No recommendations appearing
Check your `.env` file has the correct `GROQ_API_KEY` and the vector store has been built successfully.

### Docker container issues
Ensure the `chroma_db/` folder exists and contains data before building the Docker image.

## 📈 Future Enhancements

- [ ] Add user ratings and feedback system
- [ ] Implement collaborative filtering
- [ ] Support for multiple languages
- [ ] Add anime streaming links
- [ ] User authentication and preference storage
- [ ] Advanced filtering (by year, studio, rating)
- [ ] Recommendation explanation feature