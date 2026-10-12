from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Cơ sở dữ liệu câu hỏi được lưu an toàn trên Server (Tuyệt đối không gửi phần 'correct' và 'explanation' xuống Client)
QUESTIONS_DB = {
    1: {
        "question": "Which underlined part is pronounced differently? A. challenge B. chocolate C. achievement D. chemistry",
        "options": {"A": "challenge", "B": "chocolate", "C": "achievement", "D": "chemistry"},
        "correct": "D",
        "explanation": "Chemistry phát âm là /k/, trong khi các từ còn lại phát âm là /tʃ/[cite: 1]."
    },
    2: {
        "question": "Which underlined part is pronounced differently? A. treatment B. measure C. treasure D. pleasure",
        "options": {"A": "treatment", "B": "measure", "C": "treasure", "D": "pleasure"},
        "correct": "A",
        "explanation": "Treatment phát âm là /iː/, trong khi các từ còn lại phát âm là /e/[cite: 1]."
    },
    3: {
        "question": "Which underlined part is pronounced differently? A. explain B. entertain C. certain D. training",
        "options": {"A": "explain", "B": "entertain", "C": "certain", "D": "training"},
        "correct": "C",
        "explanation": "Certain có phần gạch chân phát âm khác biệt so với âm đôi /eɪ/ ở các từ còn lại[cite: 1]."
    },
    4: {
        "question": "Which underlined part is pronounced differently? A. leather B. cleaner C. heading D. healthcare",
        "options": {"A": "leather", "B": "cleaner", "C": "heading", "D": "healthcare"},
        "correct": "B",
        "explanation": "Cleaner phát âm là /iː/, trong khi các từ còn lại phát âm là /e/[cite: 1]."
    },
    5: {
        "question": "Which underlined part is pronounced differently? A. message B. package C. advantage D. webpage",
        "options": {"A": "message", "B": "package", "C": "advantage", "D": "webpage"},
        "correct": "D",
        "explanation": "Webpage phát âm đuôi là /eɪdʒ/, trong khi các từ còn lại có âm /ɪdʒ/[cite: 1]."
    },
    6: {
        "question": "Which word is stressed differently from the others? A. ambulance B. gathering C. connection D. salary",
        "options": {"A": "ambulance", "B": "gathering", "C": "connection", "D": "salary"},
        "correct": "C",
        "explanation": "Connection có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1[cite: 1]."
    },
    7: {
        "question": "Which word is stressed differently from the others? A. confidence B. attendance C. principle D. temporary",
        "options": {"A": "confidence", "B": "attendance", "C": "principle", "D": "temporary"},
        "correct": "B",
        "explanation": "Attendance có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1[cite: 1]."
    },
    8: {
        "question": "Which word is stressed differently from the others? A. authority B. photography C. experiment D. temporary",
        "options": {"A": "authority", "B": "photography", "C": "experiment", "D": "temporary"},
        "correct": "D",
        "explanation": "Temporary có trọng âm rơi vào âm tiết thứ 1, các từ còn lại rơi vào âm tiết thứ 2[cite: 1]."
    },
    9: {
        "question": "Which word is stressed differently from the others? A. luxury B. monument C. museum D. specialty",
        "options": {"A": "luxury", "B": "monument", "C": "museum", "D": "specialty"},
        "correct": "C",
        "explanation": "Museum có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1[cite: 1]."
    },
    10: {
        "question": "Which word is stressed differently from the others? A. consumer B. financial C. creator D. imagine",
        "options": {"A": "consumer", "B": "financial", "C": "creator", "D": "imagine"},
        "correct": "D",
        "explanation": "Imagine có trọng âm rơi vào âm tiết thứ 2, tương tự các từ consumer, financial, creator[cite: 1]."
    },
    12: {
        "question": "For health or weight loss ..., many people cut down or just stopped consuming alcoholic drinks altogether.",
        "options": {"A": "improvements", "B": "arguments", "C": "reasons", "D": "trends"},
        "correct": "C",
        "explanation": "Dùng cấu trúc cụm từ 'For health or weight loss reasons' (Vì lý do sức khỏe hoặc giảm cân)[cite: 1]."
    },
    13: {
        "question": "The cost of everything - from fuel to food seems to be rising around the world. So, growing our own food is a good way to ... money.",
        "options": {"A": "make", "B": "save", "C": "waste", "D": "share"},
        "correct": "B",
        "explanation": "Cụm từ 'save money' có nghĩa là tiết kiệm tiền[cite: 1]."
    },
    14: {
        "question": "Music is an important art form for Cuba because Cubans use music as an ... of the Cuban style.",
        "options": {"A": "impression", "B": "expression", "C": "exhibition", "D": "installation"},
        "correct": "B",
        "explanation": "'Expression' có nghĩa là sự thể hiện, sự diễn đạt phong cách[cite: 1]."
    },
    15: {
        "question": "Mixing traditional Asian ingredients with European or American pastries is a way for young Asian Americans to celebrate their ...",
        "options": {"A": "majority", "B": "identity", "C": "maturity", "D": "passivity"},
        "correct": "B",
        "explanation": "'Cultural identity' mang ý nghĩa là bản sắc văn hóa[cite: 2]."
    },
    31: {
        "question": "I've always liked taking photos. I think when I grow up, ... a professional photographer.",
        "options": {"A": "I'll be", "B": "I won't be", "C": "I'm be", "D": "I not be"},
        "correct": "A",
        "explanation": "Dùng thì tương lai đơn với 'I think' để diễn tả dự đoán cá nhân trong tương lai[cite: 2]."
    },
    32: {
        "question": "'Impression management' is the way people try ... how other people feel about them by speaking or behaving in certain ways.",
        "options": {"A": "changing", "B": "to change", "C": "to changing", "D": "changed"},
        "correct": "B",
        "explanation": "Cấu trúc 'try to do something' diễn tả sự cố gắng làm việc gì đó[cite: 2]."
    },
    35: {
        "question": "One way to avoid ... money is to wait for 30 days before you make any purchasing decisions.",
        "options": {"A": "to waste", "B": "to wasting", "C": "wasting", "D": "be wasting"},
        "correct": "C",
        "explanation": "Sau động từ 'avoid' ta sử dụng danh động từ (V-ing): avoid doing sth[cite: 2]."
    },
    46: {
        "question": "Around the age of sixteen, you must ... one of the biggest decisions of your life.",
        "options": {"A": "get", "B": "take", "C": "make", "D": "go"},
        "correct": "C",
        "explanation": "Cụm cố định 'make a decision' có nghĩa là đưa ra quyết định[cite: 3]."
    }
}

@app.route('/')
def index():
    # Chỉ trích xuất câu hỏi và các lựa chọn để gửi xuống Client, hoàn toàn giấu 'correct' và 'explanation'
    client_questions = {}
    for q_id, q_data in QUESTIONS_DB.items():
        client_questions[q_id] = {
            "question": q_data["question"],
            "options": q_data["options"]
        }
    return render_template('index.html', questions=client_questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.json.get("answers", {})
    results = {}
    score = 0
    total = len(QUESTIONS_DB)

    for q_id_str, user_ans in user_answers.items():
        q_id = int(q_id_str)
        if q_id in QUESTIONS_DB:
            correct_ans = QUESTIONS_DB[q_id]["correct"]
            is_correct = (user_ans == correct_ans)
            if is_correct:
                score += 1
            
            # Chỉ trả về kết quả chi tiết sau khi người dùng đã nộp bài
            results[q_id] = {
                "is_correct": is_correct,
                "correct": correct_ans,
                "explanation": QUESTIONS_DB[q_id]["explanation"]
            }

    return jsonify({
        "score": score,
        "total": total,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True)