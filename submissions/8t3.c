#include<stdio.h>
#include<stdbool.h>
#include<string.h>
#include<ctype.h>

int main()
{
    bool digit_seen[10] = {false};
    char input[100]; //宣告一個字串來儲存使用者輸入
    int digit; //宣告一個整數來儲存從字元轉換來的位數

    printf("Enter a number: ");

    if(fgets (input, 100, stdin) == NULL)
    {
        return 1;
    }

    for (int i = 0; input[i] != '\0' ; i++)
    {
        char current_char = input[i];

        if (current_char == '\n' || current_char == '-')
        {
            continue;
        }

        if(isdigit(current_char))
        {
            digit = current_char - '0';

            if (digit_seen[digit])
            {
                printf("Repeated digit");
                return 0;
            }

            digit_seen[digit] = true;
        }

    }
    printf("No repeated digit");

    return 0;
}