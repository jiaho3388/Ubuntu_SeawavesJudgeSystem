#include<stdio.h>
int main(){
    int a;
    char b[1000];
    int len=0;
    while (1){
        scanf("%c",&a);
        if(a<='z' && a>='a'){
            a=a-32;
        }
        if(a=='\n'){
            break;
        }
        switch(a){
    case 'A':
        a='4';
        b[len++]=a;
        break;
    case 'B':
        a='8';
        b[len++]=a;
        break;
    case 'E':
        a='3';
        b[len++]=a;
        break;
    case 'I':
        a='1';
        b[len++]=a;
        break;
    case 'O':
        a='0';
        b[len++]=a;
        break;
    case 'S':
        a='5';
        b[len++]=a;
        break;
    default:
        b[len++]=a;
        break;
}


    }
for(int i=0;i<len;i++){
    printf("%c",b[i]);
}
printf("!!!!!!!!!!");
printf("%d",len);



}
