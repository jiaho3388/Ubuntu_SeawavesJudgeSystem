#include<stdio.h>

int a(int array[], int n)
{
    int sum = 0;

    for(int i = 0; i < n; i++)
    {
        sum += array[i];
    }

    return sum;
}

int main()
{
    int n, i ,total;
    int array[100];

    scanf("%d", &n);
    for(i = 0; i < n; i++)
    {
        scanf("%d", &array[i]);
    }

    total = a(array, n);
    printf("%d", total);

    return 0;

}