#include <stdio.h>

#define MAX_LENGTH 200

int main() {
    char sentence[MAX_LENGTH];
    char terminator = ' '; // 初始化，以防萬一
    char ch;
    int i = 0;
    int end_of_word_index;
    int start_of_word_index;
    int j, k;

    // --- 步驟 1: 讀取句子 ---
    while (i < MAX_LENGTH - 1) {
        ch = getchar();

        // 檢查是否為終止符號
        // 同時檢查 EOF (檔案結尾) 和換行，讓程式更健壯
        if (ch == EOF || ch == '\n') {
            if (i > 0) { // 如果有讀到東西，我們猜測結尾
                 // 題目說一定有 . ? !，但如果測試資料沒有...
                 // 為了安全，我們預設一個空白，雖然這不太好
                 // 更好的做法是假設 . ? ! 之一
                 // 但我們還是先照著提示的邏輯
            }
            break; // 讀到結尾就跳出
        }

        if (ch == '.' || ch == '?' || ch == '!') {
            terminator = ch; // 儲存終止符號
            break; // 跳出讀取迴圈
        }

        sentence[i] = ch;
        i++;
    }

    // --- 步驟 2: 反向印出單字 (沒有提示) ---
    end_of_word_index = i; 

    for (j = i - 1; j >= -1; j--) { 
        if (j == -1 || sentence[j] == ' ') {
            
            start_of_word_index = j + 1;

            // 印出單字
            for (k = start_of_word_index; k < end_of_word_index; k++) {
                putchar(sentence[k]);
            }

            end_of_word_index = j;

            // 在單字間印出空白
            if (j > -1) {
                putchar(' ');
            }
        }
    }

    // --- 步驟 3: 印出終止符號 ---
    if (terminator != ' ') { // 只有在我們真的有存到 . ? ! 時才印
        putchar(terminator);
    }

    return 0;
}