#include<stdio.h>
#include<string.h>

int main()
{
    char message[100];
    int shift, i;
    char ch;

    printf("Enter message to be encrypted: \n");

    fgets(message, sizeof(message), stdin);

    printf("Enter shift amount (1-25): \n");

    scanf("%d", &shift);
    printf("Encrypted message: ");

    for(i = 0; i < strlen(message); i++)
    {
        ch = message[i];

        if (ch >= 'A' && ch <= 'Z') {
            // 是大寫，套用大寫字母的加密公式
            // 這就是提示中的公式！
            ch = ((ch - 'A') + shift) % 26 + 'A';
        }

        else if (ch >= 'a' && ch <= 'z') {
            // 是小寫，套用小寫字母的加密公式
            // (跟大寫公式一模一樣，只是 'A' 換成 'a')
            ch = ((ch - 'a') + shift) % 26 + 'a';
        }

        putchar(ch);
    }

    return 0;
}