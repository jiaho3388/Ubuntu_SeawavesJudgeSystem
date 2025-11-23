#include<stdio.h>
int main(){
    int i=0;
    printf("Enter message: ");
    char ch,str[100];
    while((ch=getchar())!=EOF&&ch!='\n'){
        if(ch>='a'&&ch<='z'){
            ch -= 32;
        }
        switch(ch){
            case 'A':str[i]='4';break;
            case 'B':str[i]='8';break;
            case 'E':str[i]='3';break;
            case 'I':str[i]='1';break;
            case 'O':str[i]='0';break;
            case 'S':str[i]='5';break;
            default :str[i]=ch;break;
        }
        i++;
    }
    str[i]='\0';
    printf("\nIn B1FF-speak: %s!!!!!!!!!!",str);
}
//A->4, B->8, E->3, I->1, O->0, S->5;
//Hey dude, C is rilly cool
//H3Y DUD3, C 15 R1LLY C00L!!!!!!!!!!