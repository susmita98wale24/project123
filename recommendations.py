import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import SearchHistory, Book

# Content-Based Recommendations
def recommend_books_content_based(user):
    """
    Recommend books based on the user's recent search history using content-based filtering.
    """
    # Fetch the user's recent search history
    search_histories = SearchHistory.objects.filter(user=user).order_by('-timestamp')[:10]
    queries = [history.query for history in search_histories]

    # Fetch all books from the database
    books = Book.objects.all()
    book_data = [{'id': book.id, 'title': book.title, 'author': book.author, 'category': book.category} for book in books]
    book_df = pd.DataFrame(book_data)

    # Combine all book details for TF-IDF
    if queries:
        book_df['combined'] = book_df['title'] + ' ' + book_df['author'] + ' ' + book_df['category']
        search_text = ' '.join(queries)

        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([search_text] + book_df['combined'].tolist())
        query_vector = tfidf_matrix[0]  # First row is the user's search context

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix[1:]).flatten()
        book_df['similarity'] = cosine_similarities

        # Return top 5 recommendations
        recommendations = book_df.sort_values(by='similarity', ascending=False).head(5)
        return recommendations[['id', 'title', 'author', 'category']].to_dict(orient='records')
    return []

# Collaborative Recommendations (Placeholder)
def recommend_books_collaborative(user):
    """
    Placeholder for collaborative filtering recommendations.
    Example: Use a user-item interaction matrix.
    """
    return []

# Hybrid Recommendations
def recommend_books_hybrid(user):
    """
    Combine content-based and collaborative filtering for hybrid recommendations.
    """
    content_recommendations = recommend_books_content_based(user)
    collaborative_recommendations = recommend_books_collaborative(user)

    # Combine and deduplicate recommendations
    combined_recommendations = content_recommendations + collaborative_recommendations
    unique_recommendations = {rec['id']: rec for rec in combined_recommendations}.values()

    return list(unique_recommendations)