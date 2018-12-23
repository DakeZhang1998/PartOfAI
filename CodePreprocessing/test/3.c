#include<stdlib.h>
struct entity_3{};
int main(){
int entity_1=rand();

const int entity_2 = 100 ; 
static struct entity_3 entity_4 [ entity_2 ] ; 
unsigned long long entity_5 ; 
static unsigned long long entity_6 [ entity_2 ] ; 
pthread_mutex_lock( & entity_4 [ entity_1 ] ) ; 
entity_5 = entity_6 [ entity_1 ] ; 
pthread_mutex_unlock( & entity_4 [ entity_1 ] ) ; 
return 0;
}
