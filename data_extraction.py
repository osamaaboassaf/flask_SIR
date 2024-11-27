import requests
from bs4 import BeautifulSoup
import sqlite3

def extract_and_save_faqs():
    urls = [
        "https://www.dubaitourism.gov.ae/ar/faqs",
        "https://www.dubaitourism.gov.ae/en/faqs"
    ]

    # إنشاء قاعدة بيانات
    conn = sqlite3.connect("faqs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        language TEXT
    )
    """)

    # استخراج البيانات
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # تعديل بناءً على بنية الموقع
        faqs = soup.select(".faq-item")  # تحتاج لتحديد الفئة الصحيحة
        for faq in faqs:
            question = faq.select_one(".question").get_text(strip=True)
            answer = faq.select_one(".answer").get_text(strip=True)
            language = "ar" if "ar" in url else "en"
            
            # حفظ البيانات
            cursor.execute("INSERT INTO faqs (question, answer, language) VALUES (?, ?, ?)", (question, answer, language))

    conn.commit()
    conn.close()
    print("Data extracted and saved successfully!")

# تشغيل الوظيفة
if __name__ == "__main__":
    extract_and_save_faqs()
