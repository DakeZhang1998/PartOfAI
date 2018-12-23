#include<stdlib.h>
struct var_1 { } ;
struct var_2 { } ;
struct var_3 { } ;
struct var_4 { int var_5 ; } ;
struct var_6 { int var_5 ; } ;
int main() {
int type int * var_7 = rand() ;
int * var_8 = rand() ;
int * var_9 = rand() ;

const int var_10 = 100 ; 
static struct var_11 var_12 [ var_10 ] ; 
static struct var_13 var_14 [ var_10 ] ; 
static struct var_15 var_16 [ var_10 ] ; 
static struct var_15 var_17 [ var_10 ] ; 
static struct var_18 * var_19 [ var_10 ] ; 
static unsigned long long var_20 [ var_10 ] ; 
pthread_mutex_lock ( & var_14 [ var_21 ] ) ; 
var_20 [ var_21 ] ++ ; 
pthread_mutex_unlock ( & var_14 [ var_21 ] ) ; 
pthread_cond_signal ( & var_16 [ var_21 ] ) ;return 0; 
 }