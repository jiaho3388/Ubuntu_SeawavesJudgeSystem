from flask import Flask, request, render_template_string, jsonify
import os
from judge_core import run_judge

app = Flask(__name__)

UPLOAD_FOLDER = 'submissions'
PROBLEMS_FOLDER = 'problems'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROBLEMS_FOLDER, exist_ok=True)

# 題目資料庫
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
    "note": {"title": "⚠️備註 (Remarks)", "title_zh": "補充說明", "desc": "【補充說明】\n以下題目也是期中考範圍 但是都在課本 無法提供測資\nChapter 11 Exercises 3-8 (page255-256)\nChapter 12 Projects 2 (page 275-276)\n\n有bug請回報IG : jiahedai  我醒啦 20251123 06:40編輯", "submit": False}
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌊 Seawaves Online Judge</title>
    <style>
        :root {
            --primary-color: #4a90e2;
            --bg-color: #f0f2f5;
            --card-bg: #ffffff;
            --text-color: #333;
            --term-bg: #1e1e1e;
            --term-text: #00ff00;
            --desc-bg: #fffbe6;
            --desc-border: #ffe58f;
            --danger-color: #ff4d4f;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 40px 20px;
            color: var(--text-color);
            display: flex;
            justify-content: center;
        }
        .container {
            background: var(--card-bg);
            width: 100%;
            max-width: 800px;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; color: var(--primary-color); margin-bottom: 30px; font-size: 2.2rem; }
        .form-group { margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; font-weight: 600; color: #555; font-size: 1.1rem; }
        
        select { width: 100%; padding: 14px; border: 2px solid #e1e1e1; border-radius: 8px; font-size: 18px; background-color: #fff; cursor: pointer; }
        option { font-size: 18px; padding: 10px; }
        
        input[type="file"] { width: 100%; padding: 12px; border: 2px solid #e1e1e1; border-radius: 8px; font-size: 16px; box-sizing: border-box; }
        select:focus { border-color: var(--primary-color); outline: none; }
        
        button.submit-btn {
            width: 100%; padding: 15px; background: linear-gradient(135deg, #4a90e2 0%, #007bff 100%);
            color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer;
            transition: transform 0.1s, box-shadow 0.3s;
        }
        button.submit-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(74, 144, 226, 0.4); }

        #problem-desc-container { background-color: var(--desc-bg); border: 1px solid var(--desc-border); border-radius: 8px; padding: 20px; margin-bottom: 25px; display: none; }
        
        .lang-switch { display: flex; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid #ffe58f; padding-bottom: 10px; }
        .lang-btn { padding: 6px 18px; border: 1px solid #ccc; background: #fff; border-radius: 20px; cursor: pointer; font-size: 1rem; transition: all 0.2s; }
        .lang-btn.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }
        .lang-btn.disabled { background: #e0e0e0; color: #999; border-color: #e0e0e0; cursor: not-allowed; pointer-events: none; }

        #problem-desc-content { white-space: pre-wrap; line-height: 1.6; color: #444; font-size: 1.05rem; }

        .result-box {
            margin-top: 30px; background: var(--term-bg); color: var(--term-text);
            padding: 20px; border-radius: 8px; font-family: 'Consolas', 'Monaco', monospace;
            white-space: pre-wrap; line-height: 1.5; border-left: 5px solid var(--primary-color);
            position: relative;
        }
        .result-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #444; padding-bottom: 10px; margin-bottom: 10px; }
        .btn-clear { background: transparent; border: 1px solid var(--danger-color); color: var(--danger-color); border-radius: 4px; padding: 4px 12px; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; }
        .btn-clear:hover { background: var(--danger-color); color: white; }
        
        .problem-badge {
            font-size: 0.9rem; color: #ccc; margin-left: 10px; font-weight: normal;
        }

        .footer { text-align: center; margin-top: 30px; color: #888; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌊 Seawaves Online Judge System</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            
            <div class="form-group">
                <label for="problem_id">📚 選擇題目 (Select Problem)</label>
                <select name="problem_id" id="problem_id" onchange="loadProblemInfo()">
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
                <span>
                    📊 System Output: 
                    {% if selected_pid %}
                    <span class="problem-badge">
                        ( 題目 #{{ selected_pid }} - {{ problem_title }} )
                    </span>
                    {% endif %}
                </span>
                <button type="button" class="btn-clear" onclick="clearResult()">🗑️ 清空結果</button>
            </div>
            {{ result }}
        </div>
        {% endif %}

        <div class="footer">
            Powered by AWS EC2 & Flask
        </div>
    </div>

    <script>
        let currentProblemId = '';

        window.onload = function() {
            const selectedPid = "{{ selected_pid }}";
            if (selectedPid) {
                const select = document.getElementById("problem_id");
                select.value = selectedPid;
                loadProblemInfo();
            }
        }

        function clearResult() {
            const resultBox = document.getElementById('result-container');
            if (resultBox) resultBox.style.display = 'none';
        }

        function loadProblemInfo() {
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

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    selected_pid = ""
    problem_title = ""
    
    if request.method == 'POST':
        if 'file' not in request.files: return 'No file part'
        file = request.files['file']
        problem_id = request.form.get('problem_id')
        selected_pid = problem_id 
        
        # 取得題目名稱 (用於顯示在結果視窗)
        if problem_id in PROBLEMS:
            problem_title = PROBLEMS[problem_id]['title']
        
        if not problem_id: return "⚠️ Error: 請選擇一個題目！"
        
        can_submit = PROBLEMS.get(problem_id, {}).get('submit', True)
        if not can_submit:
            return render_template_string(HTML_TEMPLATE, result="⚠️ 此題目不提供評測功能。", problems=PROBLEMS, selected_pid=selected_pid, problem_title=problem_title)

        if file.filename == '': return 'No selected file'
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            result = run_judge(problem_id, filepath)
    
    return render_template_string(HTML_TEMPLATE, result=result, problems=PROBLEMS, selected_pid=selected_pid, problem_title=problem_title)

@app.route('/problem_info/<problem_id>')
def problem_info(problem_id):
    zh_path = os.path.join(PROBLEMS_FOLDER, f"{problem_id}_zh.txt")
    en_path = os.path.join(PROBLEMS_FOLDER, f"{problem_id}_en.txt")
    has_zh = os.path.exists(zh_path)
    has_en = os.path.exists(en_path)
    
    can_submit = PROBLEMS.get(problem_id, {}).get('submit', True)
    default_desc = PROBLEMS.get(problem_id, {}).get('desc', '')
    
    content = "⚠️ 暫無題目說明"
    active_lang = 'none' # 用來告訴前端現在顯示的是哪種語言

    # --- 修改後的邏輯開始 ---
    # 優先順序 1: 英文檔案
    if has_zh:
        with open(zh_path, 'r', encoding='utf-8') as f:
            content = f.read()
        active_lang = 'zh'
    elif has_en:
        with open(en_path, 'r', encoding='utf-8') as f:
            content = f.read()
        active_lang = 'en'
    # 優先順序 2: 中文檔案 (如果沒有英文)
    
    # 優先順序 3: 字典裡的簡短描述 (如果都沒有檔案)
    elif default_desc:
        content = default_desc
        active_lang = 'none'
    # --- 修改後的邏輯結束 ---

    return jsonify({
        "has_zh": has_zh,
        "has_en": has_en,
        "content": content,
        "active_lang": active_lang, # 新增這個欄位傳給前端
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
    app.run(host='127.0.0.1', port=5000, debug=True)