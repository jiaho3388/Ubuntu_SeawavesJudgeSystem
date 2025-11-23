import requests
import re
import os
import shutil

# 你的 GitHub 檔案 (Raw 格式)
GITHUB_URL = "https://raw.githubusercontent.com/jiaho3388/20251124_CMidtermTestCase/main/testcase_3.0.md"
BASE_DIR = "testcases"

def clean_content(text):
    """清理 Markdown 格式，還原成純文字"""
    # 1. 先把 HTML 換行轉成真實換行
    text = text.replace('<br>', '\n')
    
    # 2. ★ 修改重點：直接把所有的反引號 ` 刪掉
    # (原本只刪頭尾，現在只要看到 ` 就刪掉，避免殘留在換行中間)
    text = text.replace('`', '')
    
    # 3. 去除前後空白
    return text.strip()

def main():
    print(f"📥 正在從 GitHub 下載測資...\n🔗 URL: {GITHUB_URL}")
    try:
        response = requests.get(GITHUB_URL)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"❌ 下載失敗: {e}")
        return

    # 如果 testcases 資料夾不存在則建立
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    # 依據 "## #ID" 切割題目
    problems = re.split(r'## #(\d+):', content)
    
    count = 0
    
    # split 後: [前言, ID, 內容, ID, 內容...]
    for i in range(1, len(problems), 2):
        p_id = problems[i]
        p_body = problems[i+1]
        
        # 建立題目資料夾
        p_dir = os.path.join(BASE_DIR, p_id)
        if os.path.exists(p_dir):
            shutil.rmtree(p_dir) # 清除舊的
        os.makedirs(p_dir)
        
        print(f"⚙️ 正在處理題目 #{p_id}...", end=" ")
        
        case_count = 0
        
        # 先把每一行表格抓出來
        lines = p_body.split('\n')
        for line in lines:
            # 檢查這行是不是資料行 (以 "| 數字 |" 開頭)
            match = re.search(r'\|\s*\d+\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', line)
            if match:
                case_count += 1
                raw_in = match.group(1)
                raw_out = match.group(2)
                
                # 清理並轉換
                real_in = clean_content(raw_in)
                real_out = clean_content(raw_out)
                
                # 寫入檔案
                with open(os.path.join(p_dir, f"{case_count}.in"), "w", encoding="utf-8") as f:
                    f.write(real_in)
                with open(os.path.join(p_dir, f"{case_count}.out"), "w", encoding="utf-8") as f:
                    f.write(real_out)

        print(f"✅ 已建立 {case_count} 組測資")
        count += 1

    print(f"\n🎉 全部完成！共處理了 {count} 個題目的測資。")
    print(f"📂 測資已更新至 {os.path.abspath(BASE_DIR)}")

if __name__ == "__main__":
    main()