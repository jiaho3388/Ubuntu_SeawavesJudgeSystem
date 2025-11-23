#include <stdio.h>

double average(double a, double b, double c, double d);

int main(void)
{
    double x = 0, y = 0, z = 0, w = 0;
    double avg = 0;
    scanf("%lf%lf%lf%lf", &x, &y, &z, &w);
    avg = average(x, y, z, w);
    printf("%.2f", avg);

    return 0;
}

double average(double a, double b, double c, double d)
{
    return (a + b + c + d) / 4;
}
