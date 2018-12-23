#include<stdlib.h>
#include <stdlib.h>
#include <string.h>
struct pthread_mutex_t{ int i; };
struct pthread_cond_t{ int i; };
int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; }
int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; }
void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t);
void pthread_cond_signal(struct pthread_cond_t* cond_t);
unsigned long long bioWaitStepOfType(int type) {
    const int BIO_NUM_OPS = 100;
    static unsigned long long bio_pending[BIO_NUM_OPS];
    static struct pthread_mutex_t bio_mutex[BIO_NUM_OPS];
    static struct pthread_cond_t bio_step_cond[BIO_NUM_OPS];
    unsigned long long val;
    pthread_mutex_lock(&bio_mutex[type]);
    val = bio_pending[type];
    while (1) {
        pthread_cond_wait(&bio_step_cond[type],&bio_mutex[type]);
        val = bio_pending[type];
    }
    pthread_mutex_unlock(&bio_mutex[type]);
    return val;
}
