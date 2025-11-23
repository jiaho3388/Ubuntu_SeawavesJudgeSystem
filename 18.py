import os

# 📍 設定第 18 題的資料夾
TARGET_DIR = "testcases/18"

# 📍 正確的前綴 (這是你想要的最終結果)
CORRECT_PREFIX = "Enter 10 numbers:  "

# 📍 錯誤的重複前綴 (要偵測並刪除的目標)
# 注意：這裡完全照你給的字串設定
BAD_PREFIX = "Enter 10 numbers:  Enter 10 numbers: "

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"❌ 找不到資料夾: {TARGET_DIR}")
        return

    count_fixed = 0
    count_skipped = 0

    # 遍歷資料夾內所有檔案
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".out"):
            filepath = os.path.join(TARGET_DIR, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            is_modified = False

            # 1. 先檢查是不是發生了「重複前綴」的災難
            if content.startswith(BAD_PREFIX):
                print(f"🔧 發現重複前綴，正在修復: {filename}")
                # 把開頭的錯誤前綴切掉，換成正確的
                new_content = CORRECT_PREFIX + content[len(BAD_PREFIX):]
                is_modified = True
            
            # 2. 如果沒有重複，但也沒有正確的前綴 (完全沒加過的情況)
            elif not content.startswith(CORRECT_PREFIX):
                print(f"➕ 補上遺失的前綴: {filename}")
                new_content = CORRECT_PREFIX + content
                is_modified = True
            
            # 3. 寫回檔案
            if is_modified:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count_fixed += 1
            else:
                # 代表已經是正確的格式 (CORRECT_PREFIX 開頭)
                # print(f"👌 {filename} 格式正確，跳過。")
                count_skipped += 1

    print(f"\n🎉 處理完成！")
    print(f"✅ 共修正/修復了: {count_fixed} 個檔案")
    print(f"⏭️  原本就正確跳過: {count_skipped} 個檔案")

if __name__ == "__main__":
    main()