from flask import Flask, render_template, request
from search_models import vector_search, boolean_search

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["answer"]
        language = request.form["language"]
        
        conn = sqlite3.connect("faqs.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO faqs (question, answer, language) VALUES (?, ?, ?)", (question, answer, language))
        conn.commit()
        conn.close()
        return "Added successfully!"
    
    return render_template("add.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        input_question = request.form["question"]
        algorithm = request.form["algorithm"]
        language = request.form["language"]
        
        if algorithm == "vector":
            question, answer = vector_search(input_question, language)
            return render_template("result.html", question=question, answer=answer)
        elif algorithm == "boolean":
            keywords = input_question.split()
            results = boolean_search(keywords, language)
            return render_template("results.html", results=results)
        else:
            return "Unsupported algorithm!"
    
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
