#include <stdlib.h>
#include <string.h>
struct var_1 { int var_2 ; } ;
struct var_3 { int var_2 ; } ;
typedef struct var_4 { int 
var_5 
; 
char 
* 
var_6 
; 
} 
var_4;
int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; } 
int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; } 
void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t); 
void pthread_cond_signal(struct pthread_cond_t* cond_t);
int main() {

var_4 * var_7 = malloc( 16 ) ; 
if ( ! var_7 ) 
if ( ! var_7 -> var_6 ) { 
free ( var_7 ) ; 
var_7 -> var_6 = malloc( 8 ) ; 

}return 0; 
 }