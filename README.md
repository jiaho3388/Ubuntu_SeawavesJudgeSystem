# 🌊 Seawaves Online Judge System

這是一個基於 Python Flask 與 Ubuntu 環境開發的 C 語言線上評測系統 (Online Judge)。專為教學與練習設計，提供即時的程式碼編譯與測資比對功能。

## ✨ 特色功能 (Features)

* **即時評測**：上傳 `.c` 檔案後立即編譯 (GCC) 並執行測資。
* **詳細報告**：顯示每個測資點的 Pass/Fail 狀態、執行時間 (0.xx秒) 與錯誤比對。
* **隔離環境**：每個提交 (Submission) 皆有獨立的時間戳記資料夾，避免檔案衝突。
* **現代化介面**：
    * 支援 **深色模式 (Dark Mode)**。
    * 即時伺服器時間與專注計時器。
    * 響應式設計，手機電腦皆可瀏覽。
* **多語言支援**：題目說明支援中文與英文切換。

## 🛠️ 技術堆疊 (Tech Stack)

* **Backend**: Python 3, Flask
* **Frontend**: HTML5, CSS3 (Custom Theme), JavaScript (Fetch API)
* **System**: Ubuntu Linux, GCC Compiler, Shell Scripting
* **Deployment**: AWS EC2 / Gunicorn / Nginx

## 🚀 如何使用 (How to Start)

開啟瀏覽器訪問 https://seawavesjudge.ddns.net/

## 📝 作者 (Author)

* **Jiaho** - *Initial work & Maintenance*

## 📅 更新日誌 (Changelog)

詳細的更新紀錄請參閱 [CHANGELOG.md](CHANGELOG.md)
---
*Powered by Seawaves Code Studio*