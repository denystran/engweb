from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Cơ sở dữ liệu chứa NHIỀU ĐỀ THI khác nhau (Lưu trữ an toàn trên Server)
EXAMS_DB = {
    "0003": {
        "title": "English 4 - Giữa kỳ (Mã đề 0003)",
        "description": "Bộ đề ôn tập gồm phần Phát âm, Trọng âm, Từ vựng, Ngữ pháp và Đọc hiểu.",
        "questions": {
            1: {
                "question": "Which underlined part is pronounced differently? A. challenge B. chocolate C. achievement D. chemistry",
                "options": {"A": "challenge", "B": "chocolate", "C": "achievement", "D": "chemistry"},
                "correct": "D",
                "explanation": "Chemistry phát âm là /k/, trong khi các từ còn lại phát âm là /tʃ/."
            },
            2: {
                "question": "Which underlined part is pronounced differently? A. treatment B. measure C. treasure D. pleasure",
                "options": {"A": "treatment", "B": "measure", "C": "treasure", "D": "pleasure"},
                "correct": "A",
                "explanation": "Treatment phát âm là /iː/, trong khi các từ còn lại phát âm là /e/."
            },
            12: {
                "question": "For health or weight loss ..., many people cut down or just stopped consuming alcoholic drinks altogether.",
                "options": {"A": "improvements", "B": "arguments", "C": "reasons", "D": "trends"},
                "correct": "C",
                "explanation": "Dùng cụm từ cố định: 'For health or weight loss reasons' (Vì lý do sức khỏe hoặc giảm cân)."
            },
            31: {
                "question": "I've always liked taking photos. I think when I grow up, ... a professional photographer.",
                "options": {"A": "I'll be", "B": "I won't be", "C": "I'm be", "D": "I not be"},
                "correct": "A",
                "explanation": "Dùng thì tương lai đơn với 'I think' để diễn tả dự đoán cá nhân trong tương lai."
            }
        }
    },
    "0001": {
        "title": "English 4 - Cuối kỳ mẫu (Mã đề 0001)",
        "description": "Đề thi thử tổng hợp kiểm tra ngữ pháp nâng cao và từ vựng học thuật.",
        "questions": {
            1: {
                "question": "Choose the correct preposition: She has been working in this company ... five years.",
                "options": {"A": "since", "B": "for", "C": "in", "D": "during"},
                "correct": "B",
                "explanation": "Dùng 'for' đi kèm với một khoảng thời gian cụ thể (five years)."
            },
            2: {
                "question": "If I had known about the traffic jam, I ... another route.",
                "options": {"A": "will take", "B": "would take", "C": "would have taken", "D": "took"},
                "correct": "C",
                "explanation": "Câu điều kiện loại 3 diễn tả giả thiết trái ngược với quá khứ: If + Past Perfect, would have + V3/ed."
            }
        }
    }
}

@app.route('/')
def index():
    # Gửi danh sách các đề thi (chỉ gửi tiêu đề và mô tả, không gửi câu hỏi ra ngoài trang chủ)
    exam_list = {}
    for exam_id, data in EXAMS_DB.items():
        exam_list[exam_id] = {
            "title": data["title"],
            "description": data["description"],
            "total_questions": len(data["questions"])
        }
    return render_template('index.html', exams=exam_list)

@app.route('/exam/<exam_id>')
def exam_room(exam_id):
    if exam_id not in EXAMS_DB:
        return "Không tìm thấy đề thi này!", 404
    
    exam_data = EXAMS_DB[exam_id]
    # Chỉ gửi câu hỏi và các lựa chọn xuống Client, giấu hoàn toàn 'correct' và 'explanation'
    client_questions = {}
    for q_id, q in exam_data["questions"].items():
        client_questions[q_id] = {
            "question": q["question"],
            "options": q["options"]
        }
        
    return render_template('quiz.html', exam_id=exam_id, exam_title=exam_data["title"], questions=client_questions)

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
            
            # Trả về đáp án đúng và lời giải SAU KHI người dùng đã nộp bài
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
