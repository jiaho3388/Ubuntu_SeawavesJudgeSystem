import os

# 設定要修改的題目資料夾
TARGET_DIR = "testcases/02"
# 設定要補在最前面的提示文字
PREFIX = "Enter row 1: Enter row 2: Enter row 3: Enter row 4: Enter row 5: "

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"❌ 找不到資料夾: {TARGET_DIR}")
        return

    count = 0
    # 遍歷資料夾內所有檔案
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".out"):
            filepath = os.path.join(TARGET_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 檢查是否已經加過了，避免重複加
            if content.startswith("Enter row 1:"):
                print(f"⚠️ {filename} 已經修改過，跳過。")
                continue
                
            # 加上提示文字
            new_content = PREFIX + content
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
                
            print(f"✅ 已修正: {filename}")
            count += 1

    print(f"\n🎉 完成！共修正了 {count} 個檔案。")

if __name__ == "__main__":
    main()