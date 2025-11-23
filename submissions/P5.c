#include <stdio.h>

int sum_array(int a[], int n)
{
  int i, mySum = 0;
  for (i = 0; i < n; i++)
    mySum += a[i];
  return mySum;
}

int main(void)
{
  int n = 0;
  scanf("%d", &n);
  int b[n];
  for (int i = 0; i < n; i++)
    scanf("%d", &b[i]);
  printf("%d", sum_array(b, n));

  return 0;
}
