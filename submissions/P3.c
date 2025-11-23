#include <stdio.h>

void print_count(int x)
{
  printf("%d\n", x);
}

int main(void)  
{
  int n = 0;
  scanf("%d", &n);
  for (int i = n; i >= 0; --i)
    print_count(i);

  return 0;
}
