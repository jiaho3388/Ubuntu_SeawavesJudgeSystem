import subprocess
import os
import sys
import re

# 設定：編譯器與逾時時間(秒)
COMPILER = "gcc"
TIMEOUT = 2 

def run_judge(problem_id, source_file):
    # 1. 路徑設定
    base_dir = os.path.dirname(os.path.abspath(__file__))
    testcase_dir = os.path.join(base_dir, "testcases", problem_id)
    
    # 取得 source_file 所在的資料夾 (例如: .../submissions/user_Jiaho/prob_01/20231123/)
    submission_dir = os.path.dirname(os.path.abspath(source_file))

    if not os.path.exists(testcase_dir):
        return f"Error: Problem ID {problem_id} not found."

    # 2. 編譯 C 程式
    # ★ 修改處：將執行檔 (executable) 放在 submission 資料夾內，確保隔離
    executable_name = "judge_exec"
    executable = os.path.join(submission_dir, executable_name)
    
    compile_cmd = [COMPILER, source_file, "-o", executable]
    
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    if compile_proc.returncode != 0:
        return f"🔥 Compile Error (編譯失敗):\n{compile_proc.stderr}"

    # 3. 執行測資
    results = []
    if not os.path.exists(testcase_dir):
         return "Error: No test cases found."
         
    files = os.listdir(testcase_dir)
    inputs = [f for f in files if f.endswith('.in')]
    
    if not inputs:
        return "Error: No test cases found."

    # 數值排序
    try:
        inputs.sort(key=lambda f: int(re.search(r'\d+', f).group()))
    except:
        inputs.sort()

    all_passed = True
    
    for input_file in inputs:
        # 設定路徑
        output_file = input_file.replace('.in', '.out')
        expected_output_path = os.path.join(testcase_dir, output_file)
        input_path = os.path.join(testcase_dir, input_file)

        if not os.path.exists(expected_output_path):
            continue 

        # 讀取正確答案
        with open(expected_output_path, 'r', encoding='utf-8', errors='ignore') as f:
            expected_output = f.read().strip()

        # 處理輸入檔 (補換行)
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
            input_content = infile.read()
            if not input_content.endswith('\n'):
                input_content += '\n'

        # 執行使用者程式
        try:
            # 強制關閉緩衝
            run_cmd = ["stdbuf", "-o0", executable]
            
            process = subprocess.run(
                run_cmd, 
                input=input_content, 
                capture_output=True, 
                text=True, 
                timeout=TIMEOUT
            )
            user_output = process.stdout.strip()
            
            # 比對答案
            if user_output == expected_output:
                results.append(f"✅ {input_file}: Pass")
            else:
                all_passed = False
                show_got = user_output if user_output else "<Empty Output>"
                
                debug_msg = (
                    f"\n"
                    f"   🔻 [Expected]:\n{expected_output}\n"
                    f"   -----------------------------------\n"
                    f"   🔺 [Got]:\n{show_got}\n"
                )
                results.append(f"❌ {input_file}: Fail {debug_msg}")

        except subprocess.TimeoutExpired:
            all_passed = False
            results.append(f"⏳ {input_file}: Time Limit Exceeded (超時)")
        except Exception as e:
            all_passed = False
            results.append(f"⚠️ {input_file}: Runtime Error ({str(e)})")

    # 清理執行檔 (只刪除這次產生的，不會誤刪別人的)
    if os.path.exists(executable):
        os.remove(executable)

    # 總結
    final_verdict = "🎉 All Accepted!" if all_passed else "🔥 Some Failed"
    return f"{final_verdict}\n" + "\n".join(results)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 judge_core.py <problem_id> <c_file>")
    else:
        print(run_judge(sys.argv[1], sys.argv[2]))