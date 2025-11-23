#include<stdio.h>
#include<stdbool.h>
#include<ctype.h>

int main()
{
    int letter[26] = {0};
    char ch;
    bool is_anagrams = true;

    printf("Enter first word: ");
    while((ch = getchar()) != '\n' && ch != EOF)
    {
        if(isalpha(ch))
        {
            letter[tolower(ch - 'a')]++;
        }
    }

    printf("Enter second word: ");
    while((ch = getchar()) != '\n' && ch != EOF)
    {
        if(isalpha(ch))
        {
            letter[tolower(ch - 'a')]--;
        }
    }

    for(int i = 0; i < 26 ; i++)
    {
        if(letter[i] != 0)
        {
            is_anagrams = false;
            break;
        }
    }

    if(is_anagrams)
    {
        printf("The words are anagrams.");
    }
    else{
        printf("The words are not anagrams.");
    }

    return 0;

}