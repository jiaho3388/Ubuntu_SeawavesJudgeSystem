#include<stdio.h>
int sum_f(int a,int num1,int num2);
int main(){
    int a=0,sum=0;
    scanf("%d",&a);
    sum = sum_f(a,1,1);
    printf("%d",sum);
}
int sum_f(int a,int num1,int num2){
    if(a>1){
        //printf("%d %d %d\n",a,num1,num2);
        int sum = num1 + num2;
        num1 = num2;
        num2 = sum;
        return sum_f(--a,num1,num2);
    }else{
        return num2;
    }
}