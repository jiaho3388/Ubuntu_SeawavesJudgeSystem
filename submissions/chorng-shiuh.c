#include <stdio.h>
void max_min(int b[],int n, int *max, int *min){
    for(int i=1;i<n;i++){
        if(*max<b[i]){
            *max=b[i];
        }
        if(*min >b[i]){
            *min=b[i];
        }
    }
    printf("Largest: %d\n",*max);
    printf("Smallest: %d",*min);
}
int main(){
    int a;
    int b[10];
    int n=10;
    printf("Enter 10 numbers: ");
    for(int i=0;i<n;i++){
        scanf("%d",&a);
        b[i]=a;
    }
    int maxvalue=b[0];
    int minvalue=b[0];
    max_min(b, n, &maxvalue, &minvalue);
}
