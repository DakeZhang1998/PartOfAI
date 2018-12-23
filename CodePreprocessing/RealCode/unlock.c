#include<stdlib.h>
    struct pthread_t{};
    struct pthread_mutex{};
    struct pthread_mutex_t{};
    struct pthread_cond_t{};
    struct list{};
void bioCreateBackgroundJob(int type, void *arg1, void *arg2, void *arg3) {
    const int BIO_NUM_OPS=100;
    static struct pthread_t bio_threads[BIO_NUM_OPS];
    static struct pthread_mutex_t bio_mutex[BIO_NUM_OPS];
    static struct pthread_cond_t bio_newjob_cond[BIO_NUM_OPS];
    static struct pthread_cond_t bio_step_cond[BIO_NUM_OPS];
    static struct list *bio_jobs[BIO_NUM_OPS];
    static unsigned long long bio_pending[BIO_NUM_OPS];
    pthread_mutex_lock(&bio_mutex[type]);
    bio_pending[type]++;
    pthread_cond_signal(&bio_newjob_cond[type]);
    pthread_mutex_unlock(&bio_mutex[type]);
}
