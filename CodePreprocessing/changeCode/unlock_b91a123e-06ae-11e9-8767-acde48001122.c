#include<stdlib.h>
#include <string.h>
struct var_1 { } ;
struct var_2 { } ;
struct var_3 { } ;
struct var_4 { int var_5 ; } ;
struct var_6 { int var_5 ; } ;
int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; } 
int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; } 
void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t); 
void pthread_cond_signal(struct pthread_cond_t* cond_t);
int main() {
int var_7 = rand() ;
int var_8 [10] ;
int var_9 [10] ;
int var_10 [10] ;

const int var_11 = 100 ; 
static struct var_1 var_12 [ var_11 ] ; 
static struct var_4 var_13 [ var_11 ] ; 
static struct var_6 var_14 [ var_11 ] ; 
static struct var_6 var_15 [ var_11 ] ; 
static struct var_3 * var_16 [ var_11 ] ; 
static unsigned long long var_17 [ var_11 ] ; 
pthread_mutex_lock ( & var_13 [ var_7 ] ) ; 
var_17 [ var_7 ] ++ ; 
pthread_cond_signal ( & var_14 [ var_7 ] ) ; 
pthread_mutex_unlock ( & var_13 [ var_7 ] ) ;return 0; 
 }