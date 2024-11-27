from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

# النموذج الشعاعي (Vector Model)
def vector_search(input_question, language="en"):
    conn = sqlite3.connect("faqs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faqs WHERE language=?", (language,))
    data = cursor.fetchall()
    conn.close()

    questions, answers = zip(*data)

    # استخدام TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(questions + (input_question,))
    similarities = cosine_similarity(vectors[-1], vectors[:-1])
    
    # العثور على أعلى تشابه
    best_match_idx = similarities.argmax()
    return questions[best_match_idx], answers[best_match_idx]

# النموذج البولياني (Boolean Model)
def boolean_search(input_keywords, language="en"):
    conn = sqlite3.connect("faqs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faqs WHERE language=?", (language,))
    data = cursor.fetchall()
    conn.close()

    results = []
    for question, answer in data:
        if all(keyword.lower() in question.lower() for keyword in input_keywords):
            results.append((question, answer))
    return results
