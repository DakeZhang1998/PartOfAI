#include <stdlib.h>
#include <string.h>
struct var_1 { int var_2 ; } ;
struct var_3 { int var_2 ; } ;
int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; } 
int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; } 
void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t); 
void pthread_cond_signal(struct pthread_cond_t* cond_t);
int main() {
int var_4 = rand() ;

const int var_5 = 100 ; 
static unsigned long long var_6 [ var_5 ] ; 
static struct var_1 var_7 [ var_5 ] ; 
static struct var_3 var_8 [ var_5 ] ; 
unsigned long long var_9 ; 
pthread_mutex_lock ( & var_7 [ var_4 ] ) ; 
var_9 = var_6 [ var_4 ] ; 
if ( var_9 != 0 ) { 
pthread_cond_wait ( & var_8 [ var_4 ] , & var_7 [ var_4 ] ) ; 
var_9 = var_6 [ var_4 ] ; 
} 
pthread_mutex_unlock ( & var_7 [ var_4 ] ) ; return 0; 
 }