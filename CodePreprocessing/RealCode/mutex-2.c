#include<stdlib.h>
struct pthread_mutex_t{};
unsigned long long bioPendingJobsOfType(int type) {
    const int BIO_NUM_OPS = 100;
    static struct pthread_mutex_t bio_mutex[BIO_NUM_OPS];
    static unsigned long long bio_pending[BIO_NUM_OPS];
    unsigned long long val;
    pthread_mutex_unlock(&bio_mutex[type]);
    val = bio_pending[type];
    pthread_mutex_lock(&bio_mutex[type]);
    return val;
}
