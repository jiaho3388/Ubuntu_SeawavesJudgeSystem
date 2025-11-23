import os

# 設定目標資料夾
TARGET_DIR = "problems"

# 題目列表 (對應 app.py 的設定)
PROBLEMS = {
    "01": "B1FF Filter",
    "02": "5x5 Array Sums",
    "03": "Reverse Words",
    "04": "Caesar Cipher",
    "05": "Anagrams",
    "06": "Average (3 numbers)",
    "07": "Max Value",
    "08": "Sum of Array",
    "09": "Square of Asterisks",
    "10": "Max/Min Items",
    "11": "Polynomial",
    "12": "Fibonacci",
    "13": "Guess the Number",
    "15": "Poker Hand",
    "17": "Max_Min Function",
    "18": "Reverse Array"
}

def main():
    # 1. 確保資料夾存在
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"📂 已建立資料夾: {TARGET_DIR}")

    count = 0

    # 2. 遍歷所有題目 ID
    for pid, title in PROBLEMS.items():
        # --- 建立英文檔 (_en.txt) ---
        en_filename = f"{pid}_en.txt"
        en_path = os.path.join(TARGET_DIR, en_filename)
        
        if not os.path.exists(en_path):
            with open(en_path, "w", encoding="utf-8") as f:
                # 寫入預設模板內容
                f.write(f"=== Problem #{pid}: {title} ===\n\n(Please paste English description here...)")
            print(f"✅ 建立: {en_filename}")
            count += 1
        else:
            print(f"⚠️ 跳過 (已存在): {en_filename}")

        # --- 建立中文檔 (_zh.txt) ---
        zh_filename = f"{pid}_zh.txt"
        zh_path = os.path.join(TARGET_DIR, zh_filename)
        
        if not os.path.exists(zh_path):
            with open(zh_path, "w", encoding="utf-8") as f:
                # 寫入預設模板內容
                f.write(f"=== 第 #{pid} 題: {title} ===\n\n(請在此貼上中文題目說明...)")
            print(f"✅ 建立: {zh_filename}")
            count += 1
        else:
            print(f"⚠️ 跳過 (已存在): {zh_filename}")

    print(f"\n🎉 完成！共新增了 {count} 個檔案。")
    print(f"請記得到 {TARGET_DIR}/ 資料夾內編輯內容喔！")

if __name__ == "__main__":
    main()