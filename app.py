from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

EXAMS_DB = {
    "0003": {
        "title": "English 4 - Giữa Kỳ (Mã đề 0003)",
        "description": "Đề thi chính thức ngày 4 tháng 11 năm 2023 - ĐH Bách Khoa TP.HCM (HK231).",
        "duration_minutes": 50,
        "questions": {
            # --- PRONUNCIATION & STRESS (1-10) ---
            1: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "<u>ch</u>allenge", "B": "<u>ch</u>ocolate", "C": "a<u>ch</u>ievement", "D": "<u>ch</u>emistry"},
                "correct": "D", "explanation": "Chemistry phát âm là /k/, trong khi các từ còn lại phát âm là /tʃ/."
            },
            2: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "tr<u>ea</u>tment", "B": "m<u>ea</u>sure", "C": "tr<u>ea</u>sure", "D": "pl<u>ea</u>sure"},
                "correct": "A", "explanation": "Treatment phát âm là /iː/, trong khi các từ còn lại phát âm là /e/."
            },
            3: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "<u>ex</u>plain", "B": "<u>en</u>tertain", "C": "c<u>er</u>tain", "D": "tr<u>ai</u>ning"},
                "correct": "C", "explanation": "Certain có phần gạch chân phát âm khác biệt so với âm đôi /eɪ/ ở các từ còn lại."
            },
            4: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "l<u>ea</u>ther", "B": "cl<u>ea</u>ner", "C": "h<u>ea</u>ding", "D": "h<u>ea</u>lthcare"},
                "correct": "B", "explanation": "Cleaner phát âm là /iː/, trong khi các từ còn lại phát âm là /e/."
            },
            5: {
                "section": "pronunciation", "sectionName": "Phát âm",
                "question": "Which underlined part is pronounced differently?",
                "options": {"A": "m<u>e</u>ssage", "B": "p<u>a</u>ckage", "C": "adv<u>a</u>ntage", "D": "w<u>e</u>bpage"},
                "correct": "D", "explanation": "Webpage phát âm đuôi là /eɪdʒ/, trong khi các từ còn lại có âm /ɪdʒ/."
            },
            6: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "ambulance", "B": "gathering", "C": "connection", "D": "salary"},
                "correct": "C", "explanation": "Connection có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1."
            },
            7: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "confidence", "B": "attendance", "C": "principle", "D": "temporary"},
                "correct": "B", "explanation": "Attendance có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1."
            },
            8: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "authority", "B": "photography", "C": "experiment", "D": "temporary"},
                "correct": "D", "explanation": "Temporary có trọng âm rơi vào âm tiết thứ 1, các từ còn lại rơi vào âm tiết thứ 2."
            },
            9: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "luxury", "B": "monument", "C": "museum", "D": "specialty"},
                "correct": "C", "explanation": "Museum có trọng âm rơi vào âm tiết thứ 2, các từ còn lại rơi vào âm tiết thứ 1."
            },
            10: {
                "section": "stress", "sectionName": "Trọng âm",
                "question": "Which word is stressed differently from the others?",
                "options": {"A": "consumer", "B": "financial", "C": "creator", "D": "imagine"},
                "correct": "D", "explanation": "Imagine có trọng âm rơi vào âm tiết thứ 2, tương tự các từ consumer, financial, creator."
            },

            # --- VOCABULARY (11-30) ---
            11: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "The technology is designed to reduce communication delays and improve device performance, especially for ...",
                "options": {"A": "activities", "B": "events", "C": "issues", "D": "works"},
                "correct": "A", "explanation": "Dùng từ 'activities' phù hợp với ngữ cảnh cải thiện hiệu suất thiết bị cho các hoạt động."
            },
            12: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "For health or weight loss ..., many people cut down or just stopped consuming alcoholic drinks altogether.",
                "options": {"A": "improvements", "B": "arguments", "C": "reasons", "D": "trends"},
                "correct": "C", "explanation": "Cụm cố định: 'For health or weight loss reasons' (Vì lý do sức khỏe hoặc giảm cân)."
            },
            13: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "The cost of everything - from fuel to food seems to be rising around the world. So, growing our own food is a good way to ... money.",
                "options": {"A": "make", "B": "save", "C": "waste", "D": "share"},
                "correct": "B", "explanation": "Cụm từ 'save money' có nghĩa là tiết kiệm tiền."
            },
            14: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Music is an important art form for Cuba because Cubans use music as an ... of the Cuban style.",
                "options": {"A": "impression", "B": "expression", "C": "exhibition", "D": "installation"},
                "correct": "B", "explanation": "'Expression' có nghĩa là sự thể hiện, sự diễn đạt phong cách."
            },
            15: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Mixing traditional Asian ingredients with European or American pastries is a way for young Asian Americans to celebrate their ...",
                "options": {"A": "majority", "B": "identity", "C": "maturity", "D": "passivity"},
                "correct": "B", "explanation": "'Cultural identity' mang ý nghĩa là bản sắc văn hóa."
            },
            16: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Making a good loaf of bread requires patience, know-how and good ...",
                "options": {"A": "shower", "B": "power", "C": "colour", "D": "flour"},
                "correct": "D", "explanation": "'Flour' là bột mì - nguyên liệu chính để làm bánh mì."
            },
            17: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "If their websites aren't quick enough, e-commerce businesses may lose huge amounts of ...",
                "options": {"A": "profit", "B": "budget", "C": "taxes", "D": "expenses"},
                "correct": "A", "explanation": "'Lose huge profit' - thất thoát lợi nhuận lớn nếu website không đủ nhanh."
            },
            18: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "I always set a ... when I go to the supermarket to make sure I don't spend too much money.",
                "options": {"A": "limit", "B": "budget", "C": "balance", "D": "loan"},
                "correct": "B", "explanation": "Cụm từ 'set a budget' có nghĩa là thiết lập ngân sách chi tiêu."
            },
            19: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "My uncle prefers having meals out at restaurants ... sometimes. It's one of his few ...",
                "options": {"A": "thoughts", "B": "choices", "C": "luxuries", "D": "changes"},
                "correct": "C", "explanation": "'Few luxuries' chỉ những điều xa xỉ hiếm hoi mà ông ấy tận hưởng."
            },
            20: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "The apartment is located in a nice area in the city and I can ... the rent quite easily with my income.",
                "options": {"A": "earn", "B": "borrow", "C": "carry", "D": "afford"},
                "correct": "D", "explanation": "Cấu trúc 'afford the rent' có nghĩa là đủ khả năng chi trả tiền thuê nhà."
            },
            21: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Being a good manager requires a number of ... specialized skills.",
                "options": {"A": "highly", "B": "clearly", "C": "freely", "D": "simply"},
                "correct": "A", "explanation": "Trạng từ 'highly' đi với 'specialized' tạo thành cụm 'highly specialized skills' (kỹ năng chuyên môn cao)."
            },
            22: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "The new personal assistant is unable to cope with her increasing ...",
                "options": {"A": "payment", "B": "job", "C": "workload", "D": "break"},
                "correct": "C", "explanation": "'Increasing workload' nghĩa là khối lượng công việc ngày càng tăng."
            },
            23: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "One way to achieve ... is perhaps to make a clear distinction between work and private life.",
                "options": {"A": "diversity", "B": "balance", "C": "maintenance", "D": "workforce"},
                "correct": "B", "explanation": "Cụm từ 'work-life balance' chỉ sự cân bằng giữa công việc và đời tư."
            },
            24: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Many artists say they find the new museum ... and enjoy visiting it when they need new ideas.",
                "options": {"A": "emotional", "B": "inspirational", "C": "award-winning", "D": "additional"},
                "correct": "B", "explanation": "Bảo tàng mang lại sự truyền cảm hứng cho nghệ sĩ ('inspirational')."
            },
            25: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "My parents gave me a ... to buy my car, so I need to start paying them back.",
                "options": {"A": "payment", "B": "debt", "C": "saving", "D": "loan"},
                "correct": "D", "explanation": "'Loan' là khoản tiền vay mượn từ bố mẹ để mua xe."
            },
            26: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Sorry, but the coffee machine is ... out of service.",
                "options": {"A": "temporarily", "B": "rapidly", "C": "fortunately", "D": "similarly"},
                "correct": "A", "explanation": "Cụm 'temporarily out of service' có nghĩa là tạm thời ngưng hoạt động."
            },
            27: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Cosmetics are substances that you put on your face or body to ... appearance.",
                "options": {"A": "attract", "B": "repair", "C": "decorate", "D": "improve"},
                "correct": "D", "explanation": "Mỹ phẩm dùng để cải thiện ngoại hình ('improve appearance')."
            },
            28: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Reused wastewater can now ... 40% of Singapore's water demand.",
                "options": {"A": "wash", "B": "fix", "C": "manage", "D": "meet"},
                "correct": "D", "explanation": "Cụm 'meet demand' mang nghĩa đáp ứng nhu cầu."
            },
            29: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Zoom, a video-calling service that became widely used during the pandemic, says most of its ... want to come into the office part-time.",
                "options": {"A": "colleagues", "B": "employees", "C": "suppliers", "D": "relations"},
                "correct": "B", "explanation": "'Employees' là nhân viên làm việc tại công ty."
            },
            30: {
                "section": "vocabulary", "sectionName": "Từ vựng",
                "question": "Many people are trying to find more renewable forms of energy to ... their carbon footprint.",
                "options": {"A": "reduce", "B": "increase", "C": "throw away", "D": "recycle"},
                "correct": "A", "explanation": "Cụm 'reduce carbon footprint' nghĩa là giảm lượng khí thải carbon."
            },

            # --- GRAMMAR (31-45) ---
            31: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "I've always liked taking photos. I think when I grow up, ... a professional photographer.",
                "options": {"A": "I'll be", "B": "I won't be", "C": "I'm be", "D": "I not be"},
                "correct": "A", "explanation": "Dùng thì tương lai đơn với 'I think' để diễn tả dự đoán cá nhân."
            },
            32: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "'Impression management' is the way people try ... how other people feel about them by speaking or behaving in certain ways.",
                "options": {"A": "changing", "B": "to change", "C": "to changing", "D": "changed"},
                "correct": "B", "explanation": "Cấu trúc 'try to do something' diễn tả sự cố gắng làm việc gì đó."
            },
            33: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Thanks again for lending me the money. ... pay you back tomorrow.",
                "options": {"A": "I'm", "B": "I'll", "C": "I've", "D": "I'd"},
                "correct": "B", "explanation": "Dùng thì tương lai đơn (I'll) để đưa ra lời hứa hẹn tại thời điểm nói."
            },
            34: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "The price of necessities seems ... going up a lot these days.",
                "options": {"A": "to have", "B": "to be", "C": "being", "D": "to be"},
                "correct": "B", "explanation": "Cấu trúc 'seem to be + V-ing' diễn tả sự việc dường như đang diễn ra."
            },
            35: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "One way to avoid ... money is to wait for 30 days before you make any purchasing decisions.",
                "options": {"A": "to waste", "B": "to wasting", "C": "wasting", "D": "be wasting"},
                "correct": "C", "explanation": "Sau động từ 'avoid' ta dùng danh động từ (V-ing): avoid doing sth."
            },
            36: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Technology is supposed to be something that makes our lives faster. We've learnt to expect things to be available ...",
                "options": {"A": "immediately", "B": "completely", "C": "absolutely", "D": "extremely"},
                "correct": "A", "explanation": "Trạng từ 'immediately' chỉ sự sẵn có ngay lập tức."
            },
            37: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Migrants around the world still see the US ... one of the best as economic opportunities for them ... the city centre.",
                "options": {"A": "over", "B": "in", "C": "on", "D": "at"},
                "correct": "B", "explanation": "Giới từ 'in' phù hợp khi nói về vị trí địa lý hoặc không gian."
            },
            38: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Lots of marketing strategies aim at ... consumers buy unnecessary items without thinking.",
                "options": {"A": "encouraging", "B": "to encourage", "C": "to encouraging", "D": "being encouraged"},
                "correct": "A", "explanation": "Cấu trúc 'aim at doing sth' (nhắm đến mục đích làm gì)."
            },
            39: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Gluten is a protein found in wheat and some other grains. Human digestive systems cannot break ... gluten completely.",
                "options": {"A": "down", "B": "up", "C": "through", "D": "out"},
                "correct": "A", "explanation": "Cụm phrasal verb 'break down' có nghĩa là phân giải, tiêu hóa."
            },
            40: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "For centuries the native Mapuche people in Chile ... quillay trees to make soap and medicine.",
                "options": {"A": "will use", "B": "are used", "C": "have been using", "D": "were using"},
                "correct": "C", "explanation": "Dấu hiệu 'For centuries' kết hợp hành động kéo dài từ quá khứ đến hiện tại."
            },
            41: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "It's better to use the road around the city rather than ... the city centre.",
                "options": {"A": "slowly through", "B": "through slowly", "C": "carefully around", "D": "drive"},
                "correct": "A", "explanation": "Trạng từ bổ nghĩa cho hành động đi xuyên qua trung tâm."
            },
            42: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "A worldwide economic slowdown and a bad expectation for advertising ... Meta and other social media companies.",
                "options": {"A": "would hurt", "B": "have hurt", "C": "would have hurt", "D": "was hurt"},
                "correct": "B", "explanation": "Thì hiện tại hoàn thành diễn tả sự việc ở quá khứ còn ảnh hưởng đến hiện tại."
            },
            43: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "The camera upgrades aim ... it easier for users to capture higher quality pictures, especially when available light is low.",
                "options": {"A": "to make", "B": "make", "C": "to making", "D": "making"},
                "correct": "A", "explanation": "Cấu trúc 'aim to do sth' hướng tới mục đích làm gì."
            },
            44: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Walk ... the road, and don't look at your phone at the same time.",
                "options": {"A": "across carefully", "B": "carefully across", "C": "carefully around", "D": "around carefully"},
                "correct": "B", "explanation": "Trạng từ 'carefully' đứng trước bổ nghĩa cho hướng 'across the road'."
            },
            45: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "When I was in the town centre, I stopped ... a quick lunch before our meeting in the afternoon.",
                "options": {"A": "having", "B": "to having", "C": "to have", "D": "having had"},
                "correct": "C", "explanation": "Cấu trúc 'stop to do sth' có nghĩa là dừng lại để làm việc gì."
            },

            # --- CLOZE PASSAGE (46-50) ---
            46: {
                "section": "cloze", "sectionName": "Đọc điền từ",
                "question": "Around the age of sixteen, you must ... one of the biggest decisions of your life.",
                "options": {"A": "get", "B": "take", "C": "make", "D": "go"},
                "correct": "C", "explanation": "Cụm cố định 'make a decision' nghĩa là đưa ra quyết định."
            },
            47: {
                "section": "cloze", "sectionName": "Đọc điền từ",
                "question": "... Do I leave and start work or begin a training ...?",
                "options": {"A": "course", "B": "school", "C": "term", "D": "class"},
                "correct": "A", "explanation": "Cụm 'training course' có nghĩa là khóa đào tạo."
            },
            48: {
                "section": "cloze", "sectionName": "Đọc điền từ",
                "question": "... people who have the right skills will have a big ... in the competition for jobs.",
                "options": {"A": "disadvantage", "B": "advantage", "C": "benefit", "D": "con"},
                "correct": "B", "explanation": "Cụm 'have a big advantage' nghĩa là có lợi thế lớn."
            },
            49: {
                "section": "cloze", "sectionName": "Đọc điền từ",
                "question": "Getting qualifications will help you ... on more quickly in many careers...",
                "options": {"A": "get", "B": "got", "C": "gets", "D": "getting"},
                "correct": "A", "explanation": "Sau động từ 'help', ta dùng động từ nguyên mẫu không 'to' ('help you get')."
            },
            50: {
                "section": "cloze", "sectionName": "Đọc điền từ",
                "question": "... In this way, you can ... for your student days, as well as getting practical work experience.",
                "options": {"A": "waste", "B": "spend", "C": "save up", "D": "give"},
                "correct": "C", "explanation": "Cụm 'save up for' có nghĩa là tiết kiệm tiền cho mục đích gì."
            },

            # --- READING COMPREHENSION (51-60) ---
            51: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "The word 'tumultuous' in line 1 is closest in meaning to:",
                "options": {"A": "exciting", "B": "surprising", "C": "threatening", "D": "challenging"},
                "correct": "D", "explanation": "'Tumultuous' (đầy biến động) đồng nghĩa với 'challenging' trong ngữ cảnh."
            },
            52: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "What did teachers across the globe use to give lessons?",
                "options": {"A": "online platforms", "B": "television series", "C": "social media", "D": "satellite Internet"},
                "correct": "A", "explanation": "Dựa vào bài đọc: giáo viên phải sử dụng các nền tảng trực tuyến ('online platforms')."
            },
            53: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "What transformed global education during the year 2020?",
                "options": {"A": "e-books", "B": "online teachers", "C": "technology", "D": "social economy"},
                "correct": "C", "explanation": "Dựa vào bài đọc: công nghệ chiếm vị trí trung tâm ('as technology took center stage')."
            },
            54: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "What caused the difference in education quality around the world?",
                "options": {"A": "The quality of Internet connections.", "B": "The abilities of the teachers.", "C": "How well the students use technology.", "D": "All the three factors."},
                "correct": "D", "explanation": "Chất lượng giáo dục phụ thuộc vào kết nối internet, sự chuẩn bị của giáo viên và thiết bị học sinh."
            },
            55: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "Some students were still unable to learn since they ...",
                "options": {"A": "didn't have the devices", "B": "were too old", "C": "weren't able to concentrate", "D": "had no intention"},
                "correct": "A", "explanation": "Nhiều học sinh bị bỏ lỡ bài học vì thiếu máy tính, máy tính bảng hoặc điện thoại."
            },
            56: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "According to the reading, ... benefited from the new initiative in Malaysia.",
                "options": {"A": "150,000 students living in rural areas", "B": "students from 150,000 schools", "C": "150,000 students from 500 schools", "D": "500 underprivileged students"},
                "correct": "C", "explanation": "Dựa vào đoạn: '150,000 eligible pupils from 500 schools'."
            },
            57: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "The Malaysian Education Minister hoped to ...",
                "options": {"A": "be successful", "B": "export the initiative", "C": "multiply the devices", "D": "expand the programme"},
                "correct": "D", "explanation": "Bộ trưởng hy vọng mở rộng chương trình này ('expand the programme')."
            },
            58: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "One of the purposes of the initial rollout is to ...",
                "options": {"A": "set an example to other parts of the country", "B": "find a better way to expand the programme", "C": "find the best approach before the expansion of the programme", "D": "carry out some research on online programmes"},
                "correct": "C", "explanation": "Dự án thí điểm nhằm tìm ra phương pháp triển khai tốt nhất trước khi mở rộng."
            },
            59: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "Students in Malaysia without Internet access ...",
                "options": {"A": "had to take a year off", "B": "had a special distance learning programme", "C": "could borrow lessons from online friends", "D": "could use TV programmes to learn"},
                "correct": "D", "explanation": "Học sinh không có internet có thể học qua các chương trình truyền hình giáo dục."
            },
            60: {
                "section": "reading", "sectionName": "Đọc hiểu",
                "question": "The hard-of-hearing students in Malaysia could be aided by ...",
                "options": {"A": "TV programmers", "B": "sign language interpreters", "C": "TV producers", "D": "local social workers"},
                "correct": "B", "explanation": "Học sinh khiếm thính được hỗ trợ bởi phiên dịch viên ngôn ngữ ký hiệu."
            }
        }
    },
    # Thêm các đề khác với trạng thái đang cập nhật
    "0001": {
        "title": "English 4 - Giữa Kỳ (Mã đề 0001)",
        "description": "Bộ đề ôn tập đang được biên soạn thêm.",
        "duration_minutes": 50,
        "questions": {
            1: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Đề thi mã 0001 đang được cập nhật câu hỏi.",
                "options": {"A": "Đang cập nhật", "B": "Đang cập nhật", "C": "Đang cập nhật", "D": "Đang cập nhật"},
                "correct": "A",
                "explanation": "Nội dung đề thi này sẽ sớm được cập nhật."
            }
        }
    },
    "0002": {
        "title": "English 4 - Giữa Kỳ (Mã đề 0002)",
        "description": "Bộ đề ôn tập đang được biên soạn thêm.",
        "duration_minutes": 50,
        "questions": {
            1: {
                "section": "grammar", "sectionName": "Ngữ pháp",
                "question": "Đề thi mã 0002 đang được cập nhật câu hỏi.",
                "options": {"A": "Đang cập nhật", "B": "Đang cập nhật", "C": "Đang cập nhật", "D": "Đang cập nhật"},
                "correct": "A",
                "explanation": "Nội dung đề thi này sẽ sớm được cập nhật."
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
