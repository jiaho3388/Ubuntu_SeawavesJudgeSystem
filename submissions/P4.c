#include <stdio.h>

int compare(int x, int y)
{
    if (x >= y)
        return x;
    else
        return y;
}

int main(void)
{
    int a = 0, b = 0;
    scanf("%d%d", &a, &b);
    printf("%d", compare(a, b));
    return 0;
}
