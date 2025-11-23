#include<stdio.h>
int main(){
    int secret,a;
    scanf("%d",&secret);
    while(1){
        scanf("%d",&a);
        if(a<1 || a>1000){
            printf("x\n");
        }
        else if(a<secret){
            printf("Too-low\n");
        }
        else if(a>secret){
            printf("Too-high\n");
        }
        else if(a==secret){
            printf("Success\n");
            return 0;
        }


    }

}
