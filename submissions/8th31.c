#include<stdio.h>

int main()
{
    char sentence[100];
    char terminator = ' ';
    char ch;
    int i = 0;
    int j, k;
    int start, end;

    while(i < 99)
    {
        ch = getchar();

        if(ch == EOF || ch == '\n')
        {
            if(i > 0)
            {

            }
            break;
        }

        if(ch == '.' || ch == '?' || ch == '!')
        {
            terminator = ch;
            break;
        }

        sentence[i] = ch;
        i++;
    }

    end = i;

    for (j = i - 1; j > -1 ; j--)
    {
        if (j == -1 || sentence[j] == ' ')
        {
            start = j + 1;

            for (k = start; k < end; k++)
            {
                putchar(sentence[k]);
            }

            end = j;

            if(j > -1)
            {
                putchar(' ');
            }
        }
    }

    if(terminator != ' ')
    {
        putchar(terminator);
    }

    return 0;
}