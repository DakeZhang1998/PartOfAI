#include<stdlib.h> 
struct entity_4{};
struct entity_6{};
int main(){
int entity_1=rand();

const int entity_2 = 100 ; 
static unsigned long long entity_3 [ entity_2 ] ; 
static struct entity_4 entity_5 [ entity_2 ] ; 
static struct entity_6 entity_7 [ entity_2 ] ; 
unsigned long long entity_8 ; 
pthread_mutex_lock( & entity_5 [ entity_1 ] ) ; 
entity_8 = rand();
if ( rand()){ 
pthread_cond_wait( & entity_7 [ entity_1 ] , & entity_5 [ entity_1 ] ) ; 
entity_8 = rand();
} 
pthread_mutex_unlock( & entity_5 [ entity_1 ] ) ; 
return 0;
}
