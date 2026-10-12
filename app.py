from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Cơ sở dữ liệu chứa các đề thi (Lưu an toàn trên Server, không lộ đáp án khi chưa nộp bài)
EXAMS_DB = {
    "0003": {
        "title": "English 4 - Giữa Kỳ (Mã đề 0003)",
        "description": "Đề thi chính thức ngày 4 tháng 11 năm 2023 - ĐH Bách Khoa TP.HCM (HCMUT).",
        "duration_minutes": 50,
        "questions": {
            1: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "<u>ch</u>allenge", "B": "<u>ch</u>ocolate", "C": "a<u>ch</u>ievement", "D": "<u>ch</u>emistry"},
                "correct": "D",
                "explanation": "Chemistry phát âm là /k/, trong khi các từ còn lại phát âm là /tʃ/[cite: 1]."
            },
            2: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "tr<u>ea</u>tment", "B": "m<u>ea</u>sure", "C": "tr<u>ea</u>sure", "D": "pl<u>ea</u>sure"},
                "correct": "A",
                "explanation": "Treatment phát âm là /iː/, trong khi các từ còn lại phát âm là /e/[cite: 1]."
            },
            3: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "<u>ei</u>n", "B": "<u>en</u>tertain", "C": "c<u>er</u>tain", "D": "tr<u>ai</u>ning"},
                "correct": "C",
                "explanation": "Certain có phần gạch chân phát âm khác biệt so với âm đôi /eɪ/ ở các từ còn lại[cite: 1]."
            },
            4: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "l<u>ea</u>ther", "B": "cl<u>ea</u>ner", "C": "h<u>ea</u>ding", "D": "h<u>ea</u>lthcare"},
                "correct": "B",
                "explanation": "Cleaner phát âm là /iː/, trong khi các từ còn lại phát âm là /e/[cite: 1]."
            },
            5: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "m<u>e</u>ssage", "B": "p<u>a</u>ckage", "C": "adv<u>a</u>ntage", "D": "w<u>e</u>bpage"},
                "correct": "D",
                "explanation": "Webpage phát âm đuôi là /eɪdʒ/, trong khi các từ còn lại có âm /ɪdʒ/[cite: 1]."
            },
            6: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "ambulance", "B": "gathering", "C": "connection", "D": "salary"},
                "correct": "C",
                "explanation": "Connection có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1[cite: 1]."
            },
            7: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "confidence", "B": "attendance", "C": "principle", "D": "temporary"},
                "correct": "B",
                "explanation": "Attendance có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1[cite: 1]."
            },
            8: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "authority", "B": "photography", "C": "experiment", "D": "temporary"},
                "correct": "D",
                "explanation": "Temporary có trọng âm rơi vào âm tiết thứ 1, các từ còn lại rơi vào âm tiết thứ 2[cite: 1]."
            },
            9: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "luxury", "B": "monument", "C": "museum", "D": "specialty"},
                "correct": "C",
                "explanation": "Museum có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1[cite: 1]."
            },
            10: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "consumer", "B": "financial", "C": "creator", "D": "imagine"},
                "correct": "D",
                "explanation": "Imagine có trọng âm rơi vào âm tiết thứ 2, tương tự các từ consumer, financial, creator[cite: 1]."
            },
            12: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "For health or weight loss ..., many people cut down or just stopped consuming alcoholic drinks altogether.",
                "options": {"A": "improvements", "B": "arguments", "C": "reasons", "D": "trends"},
                "correct": "C",
                "explanation": "Dùng cấu trúc cụm từ 'For health or weight loss reasons' (Vì lý do sức khỏe hoặc giảm cân)[cite: 1]."
            },
            13: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "The cost of everything - from fuel to food seems to be rising around the world. So, growing our own food is a good way to ... money.",
                "options": {"A": "make", "B": "save", "C": "waste", "D": "share"},
                "correct": "B",
                "explanation": "Cụm từ 'save money' có nghĩa là tiết kiệm tiền[cite: 1]."
            },
            14: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Music is an important art form for Cuba because Cubans use music as an ... of the Cuban style.",
                "options": {"A": "impression", "B": "expression", "C": "exhibition", "D": "installation"},
                "correct": "B",
                "explanation": "'Expression' có nghĩa là sự thể hiện, sự diễn đạt phong cách[cite: 1]."
            },
            15: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Mixing traditional Asian ingredients with European or American pastries is a way for young Asian Americans to celebrate their ...",
                "options": {"A": "majority", "B": "identity", "C": "maturity", "D": "passivity"},
                "correct": "B",
                "explanation": "'Cultural identity' mang ý nghĩa là bản sắc văn hóa[cite: 2]."
            },
            31: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "I've always liked taking photos. I think when I grow up, ... a professional photographer.",
                "options": {"A": "I'll be", "B": "I won't be", "C": "I'm be", "D": "I not be"},
                "correct": "A",
                "explanation": "Dùng thì tương lai đơn với 'I think' để diễn tả dự đoán cá nhân trong tương lai[cite: 2]."
            },
            32: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "'Impression management' is the way people try ... how other people feel about them by speaking or behaving in certain ways.",
                "options": {"A": "changing", "B": "to change", "C": "to changing", "D": "changed"},
                "correct": "B",
                "explanation": "Cấu trúc 'try to do something' diễn tả sự cố gắng làm việc gì đó[cite: 2]."
            },
            46: {
                "section": "cloze", "sectionName": "Đọc điền từ",
                "question": "Around the age of sixteen, you must ... one of the biggest decisions of your life.",
                "options": {"A": "get", "B": "take", "C": "make", "D": "go"},
                "correct": "C",
                "explanation": "Cụm cố định 'make a decision' có nghĩa là đưa ra quyết định[cite: 3]."
            },
            51: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "The word 'tumultuous' in line 1 is closest in meaning to:",
                "options": {"A": "exciting", "B": "surprising", "C": "threatening", "D": "challenging"},
                "correct": "D",
                "explanation": "Từ 'tumultuous' (đầy biến động) đồng nghĩa với 'challenging' trong ngữ cảnh bài đọc[cite: 3]."
            }
        }
    },
    "final_01": {
        "title": "English 4 - Cuối Kỳ (Đang cập nhật)",
        "description": "Bộ đề thi cuối kỳ dự kiến sẽ được cập nhật đầy đủ trong thời gian tới.",
        "duration_minutes": 50,
        "questions": {
            1: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Đề thi cuối kỳ sẽ sớm được cập nhật các câu hỏi mới nhất tại đây.",
                "options": {"A": "Đang cập nhật", "B": "Đang cập nhật", "C": "Đang cập nhật", "D": "Đang cập nhật"},
                "correct": "A",
                "explanation": "Đề thi đang được biên soạn thêm."
            }
        }
    }
}

@app.route('/')
def index():
    exam_list = {}
    for exam_id, data in EXAMS_DB.items():
        exam_list[exam_id] = {
            "title": data["title"],
            "description": data["description"],
            "total_questions": len(data["questions"]),
            "duration": data["duration_minutes"]
        }
    return render_template('index.html', exams=exam_list)

@app.route('/exam/<exam_id>')
def exam_room(exam_id):
    if exam_id not in EXAMS_DB:
        return "Không tìm thấy đề thi này!", 404
    
    exam_data = EXAMS_DB[exam_id]
    # Chỉ gửi câu hỏi, lựa chọn và thời gian xuống Client, tuyệt đối giấu 'correct' và 'explanation'
    client_questions = {}
    for q_id, q in exam_data["questions"].items():
        client_questions[q_id] = {
            "section": q["section"],
            "sectionName": q["sectionName"],
            "question": q["question"],
            "options": q["options"]
        }
        
    return render_template('quiz.html', 
                           exam_id=exam_id, 
                           exam_title=exam_data["title"], 
                           duration=exam_data["duration_minutes"],
                           questions=client_questions)

@app.route('/submit/<exam_id>', methods=['POST'])
def submit_exam(exam_id):
    if exam_id not in EXAMS_DB:
        return jsonify({"error": "Invalid exam ID"}), 400
        
    user_answers = request.json.get("answers", {})
    exam_data = EXAMS_DB[exam_id]["questions"]
    
    results = {}
    score = 0
    total = len(exam_data)

    for q_id_str, user_ans in user_answers.items():
        q_id = int(q_id_str)
        if q_id in exam_data:
            correct_ans = exam_data[q_id]["correct"]
            is_correct = (user_ans == correct_ans)
            if is_correct:
                score += 1
            
            results[q_id] = {
                "is_correct": is_correct,
                "correct": correct_ans,
                "explanation": exam_data[q_id]["explanation"]
            }

    return jsonify({
        "score": score,
        "total": total,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True)
