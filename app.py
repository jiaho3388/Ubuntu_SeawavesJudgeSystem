from flask import Flask, request, render_template_string, jsonify
import os
import datetime  # 新增: 用於產生時間戳記
import markdown
from judge_core import run_judge

app = Flask(__name__)

# 設定基礎路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'submissions')
PROBLEMS_FOLDER = os.path.join(BASE_DIR, 'problems')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROBLEMS_FOLDER, exist_ok=True)

# 題目資料庫 (保持不變)
PROBLEMS = {
    "01": {"title": "B1FF Filter", "title_zh": "B1FF 過濾器", "desc": "Translate message into B1FF-speak."},
    "02": {"title": "5x5 Array Sums", "title_zh": "5x5 陣列總和", "desc": "Read 5x5 array and print row/column sums."},
    "03": {"title": "Reverse Words", "title_zh": "翻轉單字", "desc": "Reverse the words in a sentence."},
    "04": {"title": "Caesar Cipher", "title_zh": "凱薩密碼", "desc": "Encrypt message using Caesar cipher."},
    "05": {"title": "Anagrams", "title_zh": "變位字偵測", "desc": "Test whether two words are anagrams."},
    "06": {"title": "Average (3 numbers)", "title_zh": "計算平均值", "desc": "Input 3 numbers, output average."},
    "07": {"title": "Max Value", "title_zh": "找最大值", "desc": "Input 2 integers, find the maximum."},
    "08": {"title": "Sum of Array", "title_zh": "陣列加總", "desc": "Input n, then n integers, output sum."},
    "09": {"title": "Square of Asterisks", "title_zh": "星號方塊", "desc": "Display solid square of asterisks."},
    "10": {"title": "Max/Min Items", "title_zh": "陣列最大/最小值", "desc": "Find max/min items in array."},
    "11": {"title": "Polynomial", "title_zh": "多項式計算", "desc": "Compute value of polynomial."},
    "12": {"title": "Fibonacci", "title_zh": "費式數列", "desc": "Input n, output Fibonacci number Fn."},
    "13": {"title": "Guess the Number", "title_zh": "猜數字遊戲", "desc": "Game: Too-high, Too-low, Success."},
    "14": {"title": "Stack Implementation", "title_zh": "堆疊實作 (無測資)", "desc": "(本題無測資)\nImplement a stack using external variables.", "submit": False},
    "15": {"title": "Poker Hand", "title_zh": "撲克牌型判斷", "desc": "Classify a poker hand."},
    "16": {"title": "Decompose Function", "title_zh": "數值分解 (無測資)", "desc": "(本題無測資)\nDecompose a double value using pointers.", "submit": False},
    "17": {"title": "Max_Min Function", "title_zh": "最大最小值函數", "desc": "Find largest and smallest in 10 numbers."},
    "18": {"title": "Reverse Array", "title_zh": "反轉陣列", "desc": "Read 10 numbers and print in reverse order."},
    "note": {"title": "⚠️備註 (Remarks)", "title_zh": "補充說明", "desc": "【補充說明】\n以下題目也是期中考範圍 但是都在課本 無法提供測資\nChapter 11 Exercises 3-8 (page255-256)\nChapter 12 Projects 2 (page 275-276)\n\n有bug請回報IG : jiahedai  我醒啦 20251123 18:40編輯", "submit": False}
}

# ... (上面的 import 和 Flask 設定保持不變) ...

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seawaves Online Judge</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌊</text></svg>">
    <style>
        /* 定義顏色變數 (預設淺色模式) */
        :root {
            --primary-color: #4a90e2;
            --primary-hover: #357abd;
            --bg-color: #f0f2f5;
            --card-bg: #ffffff;
            --text-color: #333;
            --text-secondary: #555;
            --border-color: #e1e1e1;
            --input-bg: #ffffff;
            --term-bg: #1e1e1e;
            --term-text: #00ff00;
            --desc-bg: #fffbe6;
            --desc-border: #ffe58f;
            --desc-text: #444;
            --danger-color: #ff4d4f;
            --shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        /* 深色模式變數覆蓋 */
        [data-theme="dark"] {
            --primary-color: #64b5f6;
            --primary-hover: #42a5f5;
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-color: #e0e0e0;
            --text-secondary: #aaaaaa;
            --border-color: #333333;
            --input-bg: #2d2d2d;
            --term-bg: #000000;
            --term-text: #00ff00; /* 終端機保持綠色 */
            --desc-bg: #2a2a2a;
            --desc-border: #444;
            --desc-text: #cccccc;
            --shadow: 0 10px 25px rgba(0,0,0,0.5);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
            color: var(--text-color);
            transition: background-color 0.3s, color 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        /* 頂部資訊列樣式 */
        .info-bar {
            width: 100%;
            max-width: 800px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 10px 20px;
            background: var(--card-bg);
            border-radius: 12px;
            box-shadow: var(--shadow);
            box-sizing: border-box;
            font-size: 0.95rem;
            color: var(--text-secondary);
        }

        .info-group {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .clock-icon, .timer-icon { margin-right: 5px; }

        /* 主題切換按鈕 */
        .theme-toggle {
            background: none;
            border: 2px solid var(--border-color);
            color: var(--text-color);
            padding: 5px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 1.2rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
        }
        .theme-toggle:hover {
            border-color: var(--primary-color);
            background-color: var(--input-bg);
        }

        .container {
            background: var(--card-bg);
            width: 100%;
            max-width: 800px;
            padding: 40px;
            border-radius: 16px;
            box-shadow: var(--shadow);
            transition: background-color 0.3s, box-shadow 0.3s;
        }

        h1 { text-align: center; color: var(--primary-color); margin-bottom: 30px; font-size: 2.2rem; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: var(--text-secondary); font-size: 1.1rem; }
        
        select, input[type="text"], input[type="file"] { 
            width: 100%; padding: 14px; 
            border: 2px solid var(--border-color); 
            border-radius: 8px; font-size: 16px; 
            background-color: var(--input-bg); 
            color: var(--text-color);
            cursor: pointer; box-sizing: border-box;
            transition: border-color 0.3s;
        }
        
        select:focus, input:focus { border-color: var(--primary-color); outline: none; }
        
        button.submit-btn {
            width: 100%; padding: 15px; 
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
            color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer;
            transition: transform 0.1s, box-shadow 0.3s;
        }
        button.submit-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4); }

        #problem-desc-container { 
            background-color: var(--desc-bg); 
            border: 1px solid var(--desc-border); 
            border-radius: 8px; padding: 20px; margin-bottom: 25px; 
            display: none; 
        }
        
        .lang-switch { display: flex; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid var(--desc-border); padding-bottom: 10px; }
        .lang-btn { 
            padding: 6px 18px; border: 1px solid var(--border-color); 
            background: var(--input-bg); color: var(--text-color);
            border-radius: 20px; cursor: pointer; font-size: 1rem; transition: all 0.2s; 
        }
        .lang-btn.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }
        .lang-btn.disabled { opacity: 0.5; cursor: not-allowed; }

        #problem-desc-content { white-space: pre-wrap; line-height: 1.6; color: var(--desc-text); font-size: 1.05rem; }

        /* --- 請替換掉原本的 .result-box 相關 CSS --- */

.result-box {
    margin-top: 25px; 
    background: #1e1e1e; /* 純黑背景，更像 Terminal */
    color: #e0e0e0;      /* 淺灰文字，比全亮綠色耐看 */
    border-radius: 8px; 
    border: 1px solid #333;
    font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
    font-size: 0.9rem;   /* 字體稍微縮小 */
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    overflow: hidden;    /* 讓圓角生效 */
}

/* 頂部標題列：模仿視窗標題 */
.result-header { 
    background: #2d2d2d;
    padding: 8px 15px;
    border-bottom: 1px solid #444;
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
}

.result-title {
    font-weight: 600;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* 內容區域：緊湊排版 */
/* 修改 app.py 裡的 CSS */
.result-content {
    padding: 15px;
    line-height: 1.5;      
    max-height: 400px;     
    overflow-y: auto;      
    font-family: 'Consolas', 'Monaco', monospace; /* 確保對齊 */
    white-space: normal;   /* ★ 關鍵：改回 normal，去除 HTML 原始碼造成的空白 */
}

/* 針對「通過」與「失敗」的文字做特殊色 (這需要配合 Python 稍微改一點，或直接依賴 Emoji) */
/* 這裡主要透過縮減 padding 來減少空白 */

.btn-clear { 
    background: #444; 
    border: none; 
    color: #fff; 
    border-radius: 4px; 
    padding: 4px 10px; 
    font-size: 0.8rem; 
    cursor: pointer; 
    transition: background 0.2s;
}
.btn-clear:hover { background: #d32f2f; }

.problem-badge {
    background: #444;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    color: #aaa;
}

        .footer { text-align: center; margin-top: 30px; color: var(--text-secondary); font-size: 0.9rem; }
    </style>
</head>
<body>
    
    <div class="info-bar">
        <div class="info-group">
            <span title="現在時間">📅 <span id="clock">00:00:00</span></span>
            <span style="color: var(--border-color);">|</span>
            <span title="您已在此頁面專注了多久">⏱️ Coding: <span id="session-timer">00:00:00</span></span>
        </div>
        <button class="theme-toggle" onclick="toggleTheme()" title="切換深色/淺色模式">
            <span id="theme-icon">🌙</span>
        </button>
    </div>

    <div class="container">
        <h1>🌊 Seawaves Online Judge System 🌊</h1>
        <form action="/" method="post" enctype="multipart/form-data">

            <div class="form-group">
                <label for="problem_id">📚 選擇題目 (Select Problem)</label>
                <select name="problem_id" id="problem_id" onchange="loadProblemInfo()" required>
                    <option value="" disabled selected>請選擇題目...</option>
                    {% for pid, data in problems.items() %}
                    <option value="{{ pid }}" {% if selected_pid == pid %}selected{% endif %}>
                        {% if pid == 'note' %}
                            {{ data.title }} ({{ data.title_zh }})
                        {% else %}
                            #{{ pid }} - {{ data.title }} ({{ data.title_zh }})
                        {% endif %}
                    </option>
                    {% endfor %}
                </select>
            </div>

            <div id="problem-desc-container">
                <div class="lang-switch">
                    <button type="button" id="btn-zh" class="lang-btn active" onclick="switchLanguage('zh')">中文</button>
                    <button type="button" id="btn-en" class="lang-btn" onclick="switchLanguage('en')">English</button>
                </div>
                <div id="problem-desc-content">讀取中...</div>
            </div>
            
            <div id="submission-area">
                <div class="form-group">
                    <label for="file">💻 上傳程式碼 (Upload .c File)</label>
                    <input type="file" name="file" id="file" accept=".c">
                </div>

                <button type="submit" class="submit-btn">🚀 提交評測 (Submit Judge)</button>
            </div>
        </form>

        {% if result %}
        <div id="result-container" class="result-box">
            <div class="result-header">
                <div class="result-title">
                    <span>📋 評測報告 (Judge Report)</span>
                    {% if selected_pid %}
                    <span class="problem-badge">#{{ selected_pid }} {{ problem_title }}</span>
                    {% endif %}
                </div>
                <button type="button" class="btn-clear" onclick="clearResult()">✕ Close</button>
            </div>
            
            <div class="result-content">
                <div style="color: #888; margin-bottom: 15px; border-bottom: 1px solid #444; padding-bottom: 10px;">
                    Time: <span id="report-time"></span>
                </div>
                
                {{ result | safe }}
            </div>
        </div>
        
        <script>
            (function(){
                const now = new Date();
                const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
                const reportTime = document.getElementById('report-time');
                if(reportTime) reportTime.innerText = timeStr;
            })();
        </script>
        {% endif %}

        <div class="footer">
            Powered by AWS EC2 & Flask
        </div>
    </div>

    <script>
        let currentProblemId = '';
        let startTime = Date.now(); // 記錄進入頁面的時間

        window.onload = function() {
            const selectedPid = "{{ selected_pid }}";
            if (selectedPid) {
                const select = document.getElementById("problem_id");
                select.value = selectedPid;
                loadProblemInfo();
            }
            
            // 初始化時鐘
            setInterval(updateTime, 1000);
            updateTime();

            // 初始化計時器
            setInterval(updateSessionTimer, 1000);

            // 初始化主題
            initTheme();
        }

        // --- 時鐘與計時功能 ---
        function updateTime() {
            const now = new Date();
            // 格式化日期: YYYY-MM-DD
            const dateStr = now.toISOString().split('T')[0];
            // 格式化時間: HH:MM:SS (24小時制)
            const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
            document.getElementById('clock').innerText = `${dateStr} ${timeStr}`;
        }

        function updateSessionTimer() {
            const now = Date.now();
            const diff = Math.floor((now - startTime) / 1000);
            
            const hours = Math.floor(diff / 3600).toString().padStart(2, '0');
            const minutes = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
            const seconds = (diff % 60).toString().padStart(2, '0');
            
            document.getElementById('session-timer').innerText = `${hours}:${minutes}:${seconds}`;
        }

        // --- 深色模式功能 ---
        function initTheme() {
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
                document.getElementById('theme-icon').innerText = '☀️';
            }
        }

        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                document.getElementById('theme-icon').innerText = '🌙';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                document.getElementById('theme-icon').innerText = '☀️';
            }
        }

        // --- 原有功能保持不變 ---
        function clearResult() {
            const resultBox = document.getElementById('result-container');
            if (resultBox) resultBox.style.display = 'none';
        }

        function loadProblemInfo() {
            // ... (保持原有的 AJAX 邏輯) ...
            const select = document.getElementById("problem_id");
            currentProblemId = select.value;
            const container = document.getElementById("problem-desc-container");
            const content = document.getElementById("problem-desc-content");
            const btnZh = document.getElementById("btn-zh");
            const btnEn = document.getElementById("btn-en");
            const submissionArea = document.getElementById("submission-area");

            if (!currentProblemId) {
                container.style.display = "none";
                submissionArea.style.display = "none"; 
                return;
            }

            container.style.display = "block";
            content.innerText = "正在載入說明...";

            fetch('/problem_info/' + currentProblemId)
                .then(response => response.json())
                .then(data => {
                    if (data.can_submit) {
                        submissionArea.style.display = "block";
                        document.getElementById("file").required = true; 
                    } else {
                        submissionArea.style.display = "none";
                        document.getElementById("file").required = false; 
                    }

                    if (data.has_zh) btnZh.classList.remove('disabled'); else btnZh.classList.add('disabled');
                    if (data.has_en) btnEn.classList.remove('disabled'); else btnEn.classList.add('disabled');

                    if (data.default_desc) {
                        content.innerText = data.default_desc;
                    } else {
                        content.innerText = data.content;
                    }

                    if (data.has_zh) updateActiveButton('zh');
                    else if (data.has_en) updateActiveButton('en');
                    else updateActiveButton('none');
                })
                .catch(error => {
                    console.error('Error:', error);
                    content.innerText = "❌ 無法讀取說明";
                });
        }

        function switchLanguage(lang) {
            // ... (保持原有的 Switch Language 邏輯) ...
            if (!currentProblemId) return;
            updateActiveButton(lang);
            const content = document.getElementById("problem-desc-content");
            content.innerText = "讀取中...";
            fetch(`/get_description/${currentProblemId}/${lang}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) content.innerText = data.content;
                    else content.innerText = "⚠️ 無法讀取說明";
                });
        }

        function updateActiveButton(lang) {
            const btnZh = document.getElementById("btn-zh");
            const btnEn = document.getElementById("btn-en");
            btnZh.classList.remove('active');
            btnEn.classList.remove('active');
            if (lang === 'zh') btnZh.classList.add('active');
            if (lang === 'en') btnEn.classList.add('active');
        }
    </script>
</body>
</html>
"""

# ... (原本的 import) ...

@app.route('/', methods=['GET', 'POST'])
def index():
    # 1. ✅ [關鍵修正] 初始化所有變數 (避免 UnboundLocalError)
    result = None           # 修正報錯的關鍵
    selected_pid = ""
    problem_title = ""
    username_val = "Unknown"
    readme_html = ""
    changelog_html = ""

    # 2. 自動獲取 IP 位址 (作為使用者名稱)
    try:
        if request.headers.getlist("X-Forwarded-For"):
            user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            user_ip = request.remote_addr
        # 將 IP 的點換成底線 (e.g., 192_168_1_1)
        if user_ip:
            username_val = user_ip.replace('.', '_')
    except Exception:
        username_val = "Unknown_User"

    # 3. 讀取 Markdown 檔案 (README & CHANGELOG)
    try:
        if os.path.exists("README.md"):
            with open("README.md", "r", encoding="utf-8") as f:
                readme_html = markdown.markdown(f.read())
        
        if os.path.exists("CHANGELOG.md"):
            with open("CHANGELOG.md", "r", encoding="utf-8") as f:
                changelog_html = markdown.markdown(f.read())
    except Exception as e:
        readme_html = f"<p>Error loading info: {str(e)}</p>"

    # 4. 處理 POST 請求 (提交程式碼)
    if request.method == 'POST':
        problem_id = request.form.get('problem_id')
        selected_pid = problem_id 
        
        if problem_id in PROBLEMS:
            problem_title = PROBLEMS[problem_id]['title']
        
        # 驗證題目 ID
        if not problem_id:
            error_msg = "<span style='color: #ff4d4f; font-weight: bold;'>⚠️ Error: 請選擇一個題目 (Please select a problem)！</span>"
            return render_template_string(
                HTML_TEMPLATE, 
                result=error_msg, 
                problems=PROBLEMS, 
                selected_pid=selected_pid, 
                problem_title=problem_title, 
                username_val=username_val,
                readme_content=readme_html,
                changelog_content=changelog_html
            )

        # 檢查是否可上傳
        can_submit = PROBLEMS.get(problem_id, {}).get('submit', True)
        if not can_submit:
            return render_template_string(
                HTML_TEMPLATE, 
                result="⚠️ 此題目不提供評測功能。", 
                problems=PROBLEMS, 
                selected_pid=selected_pid, 
                problem_title=problem_title, 
                username_val=username_val,
                readme_content=readme_html,
                changelog_content=changelog_html
            )

        if 'file' not in request.files: return 'No file part'
        file = request.files['file']
        
        if file.filename == '': return 'No selected file'
        
        if file:
            # 建立資料夾 (使用 IP)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_folder = os.path.join(UPLOAD_FOLDER, f"user_{username_val}", f"prob_{problem_id}", timestamp)
            os.makedirs(save_folder, exist_ok=True)
            
            filepath = os.path.join(save_folder, "main.c") 
            file.save(filepath)
            
            # 呼叫 Judge
            result = run_judge(problem_id, filepath) 
            
            # 去除前後空白
            if result:
                result = result.strip()
    
    # 5. 回傳頁面
    return render_template_string(
        HTML_TEMPLATE, 
        result=result, 
        problems=PROBLEMS, 
        selected_pid=selected_pid, 
        problem_title=problem_title, 
        username_val=username_val,
        readme_content=readme_html,       
        changelog_content=changelog_html  
    )

    
@app.route('/problem_info/<problem_id>')
def problem_info(problem_id):
    zh_path = os.path.join(PROBLEMS_FOLDER, f"{problem_id}_zh.txt")
    en_path = os.path.join(PROBLEMS_FOLDER, f"{problem_id}_en.txt")
    has_zh = os.path.exists(zh_path)
    has_en = os.path.exists(en_path)
    
    can_submit = PROBLEMS.get(problem_id, {}).get('submit', True)
    default_desc = PROBLEMS.get(problem_id, {}).get('desc', '')
    
    content = "⚠️ 暫無題目說明"
    active_lang = 'none'

    if has_zh:
        with open(zh_path, 'r', encoding='utf-8') as f:
            content = f.read()
        active_lang = 'zh'
    elif has_en:
        with open(en_path, 'r', encoding='utf-8') as f:
            content = f.read()
        active_lang = 'en'
    elif default_desc:
        content = default_desc
        active_lang = 'none'

    return jsonify({
        "has_zh": has_zh,
        "has_en": has_en,
        "content": content,
        "active_lang": active_lang,
        "can_submit": can_submit
    })

@app.route('/get_description/<problem_id>/<lang>')
def get_description(problem_id, lang):
    filename = f"{problem_id}_{lang}.txt"
    filepath = os.path.join(PROBLEMS_FOLDER, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return jsonify({"success": True, "content": f.read()})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    else:
        return jsonify({"success": False, "error": "File not found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)