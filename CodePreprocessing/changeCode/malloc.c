#include <stdlib.h>
#include <string.h>
struct pthread_mutex_t{ int i; };
struct pthread_cond_t{ int i; };
int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; }
int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; }
void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t);
void pthread_cond_signal(struct pthread_cond_t* cond_t);
typedef struct aeApiState {
    int epfd;
    char *events;
} aeApiState;
int aeApiCreate() {
    aeApiState *state = malloc(16);
    if (!state) return -1;
    state->events = malloc(8);
    if (!state->events) {
        free(state);
        return -1;
    }
}
