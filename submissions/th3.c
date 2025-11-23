#include<stdio.h>

int sum(int n)
{
    int sum;
    int a = 1, b = 1;
    if(n == 2 || n == 1)
    {
        b = 1;
    }
    else
    {
        for(int i = 3; i < n + 1 ; i++)
        {
            sum = a + b;

            a = b;
            b = sum;
        }
    }
    
    return b;
}

int main()
{
    int a, total;
    scanf("%d", &a);
    total = sum(a);

    printf("%d", total);
    return 0;
}