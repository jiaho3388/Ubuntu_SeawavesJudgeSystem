#include<stdio.h>
#include<string.h>

int main()
{
    char message[100];
    int shift, i;
    char ch;

    printf("Enter message to be encrypted: ");
    fgets (message, sizeof(message), stdin);

    printf("Enter shift amount (1-25): ");
    scanf("%d", &shift);

    printf("Encrypted message: ");
    for(i = 0; i < strlen(message); i++)
    {
        ch = message[i];

        if(ch >= 'A' && ch <= 'Z')
        {
            ch = ((ch - 'A') + shift) % 26 + 'A';
        }
        else if(ch >= 'a' && ch <= 'z')
        {
            ch = ((ch - 'a') + shift) % 26 + 'a';
        }

        putchar(ch);
    }

    return 0;
}