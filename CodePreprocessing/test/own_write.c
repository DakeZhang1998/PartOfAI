#include<stdlib.h>

int main(){
    int a = 1;
    int b = 2;
    int c = 3;
    char d = 'c';
    int e = add(a,b);
    while(add(a,c)<4){
        a++;
    }
    b++;
    return 0;
}

int add(int a, int b){
    return a+b;
}
