#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// 定義撲克牌結構
typedef struct {
    int rank; // 點數: 2=2, ..., 9=9, t=10, j=11, q=12, k=13, a=14
    int suit; // 花色: 使用任意不同數值區分即可
} Card;

// 獲取點數的數值
int get_rank_value(char c) {
    c = tolower(c);
    if (c >= '2' && c <= '9') return c - '0';
    if (c == 't') return 10;
    if (c == 'j') return 11;
    if (c == 'q') return 12;
    if (c == 'k') return 13;
    if (c == 'a') return 14;
    return -1; // 非法字元
}

// 檢查花色是否合法 (回傳 0~3 代表花色，-1 代表錯誤)
int get_suit_value(char c) {
    c = tolower(c);
    switch(c) {
        case 'c': return 0;
        case 'd': return 1;
        case 'h': return 2;
        case 's': return 3;
        default: return -1;
    }
}

// 排序用的比較函式 (由小到大)
int compare_cards(const void *a, const void *b) {
    Card *c1 = (Card *)a;
    Card *c2 = (Card *)b;
    if (c1->rank != c2->rank) {
        return c1->rank - c2->rank;
    }
    return c1->suit - c2->suit;
}

int main() {
    Card hand[5];
    char input[5][10];
    
    // 1. 讀取輸入並檢查格式錯誤 (Type11)
    for (int i = 0; i < 5; i++) {
        if (scanf("%s", input[i]) != 1) {
            // 讀取失敗，理論上不應發生
            return 0;
        }
        
        // 檢查長度是否為 2 (例如 "ts" 是 2, "10s" 是 3 就不合法)
        if (strlen(input[i]) != 2) {
            printf("Type11");
            return 0;
        }

        int r = get_rank_value(input[i][0]);
        int s = get_suit_value(input[i][1]);

        if (r == -1 || s == -1) {
            printf("Type11");
            return 0;
        }

        hand[i].rank = r;
        hand[i].suit = s;
    }

    // 2. 檢查重複的牌 (Type10)
    for (int i = 0; i < 5; i++) {
        for (int j = i + 1; j < 5; j++) {
            if (hand[i].rank == hand[j].rank && hand[i].suit == hand[j].suit) {
                printf("Type10");
                return 0;
            }
        }
    }

    // 3. 排序手牌
    qsort(hand, 5, sizeof(Card), compare_cards);

    // 4. 分析牌型特徵
    bool is_flush = true;
    for (int i = 1; i < 5; i++) {
        if (hand[i].suit != hand[0].suit) {
            is_flush = false;
            break;
        }
    }

    bool is_straight = true;
    for (int i = 0; i < 4; i++) {
        if (hand[i+1].rank != hand[i].rank + 1) {
            is_straight = false;
            break;
        }
    }
    // 注意：題目說明 A 為最大，且順子是連續點數。
    // 依此定義，A(14) 只能接在 K(13) 後面 (10,J,Q,K,A)。
    // 不能組成 A,2,3,4,5 (因為 14 和 2 不連續)。

    // 統計點數出現次數
    int rank_counts[15] = {0}; // 索引 2~14
    for (int i = 0; i < 5; i++) {
        rank_counts[hand[i].rank]++;
    }

    int pairs = 0;      // 對子數量
    bool three = false; // 是否有三條
    bool four = false;  // 是否有四條

    for (int i = 2; i <= 14; i++) {
        if (rank_counts[i] == 2) pairs++;
        if (rank_counts[i] == 3) three = true;
        if (rank_counts[i] == 4) four = true;
    }

    // 5. 判定類別 (優先順序由高到低)
    if (is_flush && is_straight) {
        printf("Type1");
    } else if (four) {
        printf("Type2");
    } else if (three && pairs == 1) {
        printf("Type3");
    } else if (is_flush) {
        printf("Type4");
    } else if (is_straight) {
        printf("Type5");
    } else if (three) {
        printf("Type6");
    } else if (pairs == 2) {
        printf("Type7");
    } else if (pairs == 1) {
        printf("Type8");
    } else {
        printf("Type9");
    }

    // 題目要求：輸出後不可再加換行符號

    return 0;
}