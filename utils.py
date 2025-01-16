import os
import numpy as np
import joblib
from django.conf import settings
from django.http import JsonResponse
from smart_open import open as smart_open
from sklearn.metrics.pairwise import cosine_similarity

# Path to pre-trained word vectors
MODEL_PATH = os.path.join(settings.BASE_DIR, 'app', 'GoogleNews-vectors-negative300.bin')

def load_word2vec_model(model_path):
    """
    Load pre-trained Word2Vec model.
    """
    word_vectors = {}
    try:
        with smart_open(model_path, 'rb') as f:
            header = f.readline().strip().split()
            vocab_size, vector_size = int(header[0]), int(header[1])
            for _ in range(vocab_size):
                line = f.readline().decode('utf-8').strip().split()
                word = line[0]
                vector = np.array(line[1:], dtype=float)
                word_vectors[word] = vector
    except Exception as e:
        print(f"Error loading Word2Vec model: {e}")
    return word_vectors

# Load word vectors at startup
word_vectors = load_word2vec_model(MODEL_PATH)

def get_embedding(text):
    """
    Get text embedding by averaging word embeddings.
    """
    words = text.split()
    valid_vectors = [word_vectors[word] for word in words if word in word_vectors]
    if not valid_vectors:
        return None
    return np.mean(valid_vectors, axis=0)

def find_similar_books(query, books, top_n=5):
    """
    Enhanced recommendation function to find similar books.
    """
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return JsonResponse({'error': 'No valid words found in the query'}, status=400)

    book_embeddings = [
        {'title': book['title'], 'embedding': get_embedding(book['title'])}
        for book in books
    ]
    valid_books = [b for b in book_embeddings if b['embedding'] is not None]
    if not valid_books:
        return JsonResponse({'error': 'No valid embeddings for books in the dataset'}, status=400)

    similarities = [
        (book['title'], cosine_similarity([query_embedding], [book['embedding']])[0][0])
        for book in valid_books
    ]
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]
    return JsonResponse({'recommended_books': similarities}, status=200)

def load_vectorizer(vectorizer_path):
    """
    Utility function to load a vectorizer model.
    """
    try:
        return joblib.load(vectorizer_path)
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        return None

def load_lda_model(lda_path):
    """
    Utility function to load an LDA model.
    """
    try:
        return joblib.load(lda_path)
    except Exception as e:
        print(f"Error loading LDA model: {e}")
        return None

# Example view function for recommending books
def recommend_books(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)

    books = [
        {'title': 'The Great Gatsby'},
        {'title': '1984'},
        {'title': 'To Kill a Mockingbird'},
        # Add more book titles or load from database
    ]

    return find_similar_books(query, books)

def enhanced_debug_log(message, level="INFO"):
    """
    Enhanced logging for better debugging and performance tracking.
    """
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level not in levels:
        level = "INFO"
    print(f"[{level}] {message}")