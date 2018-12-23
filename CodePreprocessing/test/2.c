#include<stdlib.h> 
struct entity_6{};
struct entity_8{};
struct entity_10{};
struct entity_13{};
int main(){
int entity_1=rand();
void*entity_2;
void*entity_3;
void*entity_4;

const int entity_5 = 100 ; 
static struct entity_6 entity_7 [ entity_5 ] ; 
static struct entity_8 entity_9 [ entity_5 ] ; 
static struct entity_10 entity_11 [ entity_5 ] ; 
static struct entity_10 entity_12 [ entity_5 ] ; 
static struct entity_13 * entity_14 [ entity_5 ] ; 
static unsigned long long entity_17 [ entity_5 ] ; 
pthread_mutex_lock( & entity_9 [ entity_1 ] ) ; 
entity_17 [ entity_1 ] ++ ; 
pthread_cond_signal( & entity_11 [ entity_1 ] ) ; 
pthread_mutex_unlock( & entity_9 [ entity_1 ] ) ; 
return 0;
}
