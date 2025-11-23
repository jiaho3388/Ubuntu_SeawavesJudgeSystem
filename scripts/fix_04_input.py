import os

# 設定目標資料夾
TARGET_DIR = "testcases/04"

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"❌ 找不到資料夾: {TARGET_DIR}")
        return

    count = 0
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".in"):
            filepath = os.path.join(TARGET_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
            
            # 邏輯：從「最後一個空格」切開
            # 例如 "Hello World 13" -> "Hello World" 和 "13"
            # rsplit(' ', 1) 代表從右邊切一次
            parts = content.rsplit(' ', 1)
            
            if len(parts) == 2:
                message = parts[0]
                shift = parts[1]
                
                # 組合成兩行
                new_content = f"{message}\n{shift}"
                
                # 寫回檔案
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                print(f"✅ 已修正 {filename}: '{content}' -> 兩行")
                count += 1
            else:
                print(f"⚠️ 跳過 {filename}: 格式看起來已經是多行或無法切割")

    print(f"\n🎉 完成！共修正了 {count} 個輸入檔。")

if __name__ == "__main__":
    main()