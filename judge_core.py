import subprocess
import os
import sys
import re
import time  # 1. 引入 time 模組 (用於計時)

# 設定：編譯器與逾時時間(秒)
COMPILER = "gcc"
TIMEOUT = 2 

def run_judge(problem_id, source_file):
    # --- 路徑設定 ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    testcase_dir = os.path.join(base_dir, "testcases", problem_id)
    submission_dir = os.path.dirname(os.path.abspath(source_file))

    if not os.path.exists(testcase_dir):
        return f"<span style='color: red;'>Error: Problem ID {problem_id} not found.</span>"

    # --- 編譯 C 程式 ---
    executable_name = "judge_exec"
    executable = os.path.join(submission_dir, executable_name)
    compile_cmd = [COMPILER, source_file, "-o", executable]
    
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    if compile_proc.returncode != 0:
        return f"<div style='color: #ff4d4f; font-weight: bold;'>🔥 Compile Error (編譯失敗):</div><pre>{compile_proc.stderr}</pre>"

    # --- 準備執行測資 ---
    results_html = []
    if not os.path.exists(testcase_dir):
         return "Error: No test cases found."
         
    files = os.listdir(testcase_dir)
    inputs = [f for f in files if f.endswith('.in')]
    
    if not inputs:
        return "Error: No test cases found."

    # 排序測資 (1.in, 2.in, 10.in...)
    try:
        inputs.sort(key=lambda f: int(re.search(r'\d+', f).group()))
    except:
        inputs.sort()

    all_passed = True
    
    # --- 逐一執行測資 ---
    for idx, input_file in enumerate(inputs, start=1):
        output_file = input_file.replace('.in', '.out')
        expected_output_path = os.path.join(testcase_dir, output_file)
        input_path = os.path.join(testcase_dir, input_file)

        if not os.path.exists(expected_output_path):
            continue 

        # 讀取正確答案
        with open(expected_output_path, 'r', encoding='utf-8', errors='ignore') as f:
            expected_output = f.read().strip()

        # 讀取輸入資料
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
            input_content = infile.read()
            if not input_content.endswith('\n'):
                input_content += '\n'

        # ★★★ 開始計時 (關鍵修改) ★★★
        start_time = time.time()
        
        status = ""
        color = ""
        debug_info = ""
        duration = 0

        try:
            run_cmd = ["stdbuf", "-o0", executable]
            process = subprocess.run(
                run_cmd, 
                input=input_content, 
                capture_output=True, 
                text=True, 
                timeout=TIMEOUT
            )
            
            # ★★★ 結束計時 ★★★
            end_time = time.time()
            duration = end_time - start_time # 計算秒數差

            user_output = process.stdout.strip()
            
            # 比對結果
            if user_output == expected_output:
                status = "AC"
                color = "#52c41a" # 綠色
            else:
                all_passed = False
                status = "WA"
                color = "#ff4d4f" # 紅色
                # 錯誤資訊 (只顯示前 50 個字)
                show_got = user_output[:50] + "..." if len(user_output) > 50 else user_output
                show_got = show_got if show_got else "<Empty>"
                debug_info = f"<span style='color: #888; font-size: 0.85em; margin-left: 10px;'>Expected: {expected_output[:20]}... | Got: {show_got}</span>"

        except subprocess.TimeoutExpired:
            all_passed = False
            status = "TLE"
            color = "#faad14" # 橘黃色 (超時)
            duration = TIMEOUT # 超時就顯示最大時間
            
        except Exception as e:
            all_passed = False
            status = "RE" # Runtime Error
            color = "#ff4d4f"
            debug_info = f" ({str(e)})"

        # ★★★ 格式化顯示秒數 (小數點後兩位) ★★★
        time_str = f"{duration:.2f}s"

        # 組合 HTML： 測資 #1: AC (0.01s)
        line = (
            f"<div style='margin-bottom: 4px; font-family: monospace;'>"
            f"<span style='display:inline-block; width: 80px; color: #aaa;'>測資 #{idx}:</span>"
            f"<span style='color: {color}; font-weight: bold; width: 50px; display:inline-block;'>{status}</span>"
            f"<span style='color: #666; font-size: 0.9em;'>({time_str})</span>"
            f"{debug_info}"
            f"</div>"
        )
        results_html.append(line)

    # 清理執行檔
    if os.path.exists(executable):
        os.remove(executable)

    # 總結標題
    final_color = "#52c41a" if all_passed else "#ff4d4f"
    final_verdict = "🎉 All Accepted!" if all_passed else "🔥 Some Failed"
    summary = f"<div style='margin-bottom: 15px; font-size: 1.2em; color: {final_color}; font-weight: bold;'>{final_verdict}</div>"
    
    return summary + "".join(results_html)