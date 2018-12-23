#include <stdlib.h>
#include <string.h>
struct pthread_mutex_t{ int i; };
struct pthread_cond_t{ int i; };
int pthread_mutex_lock(struct pthread_mutex_t* mutex_t){ return 0; }
int pthread_mutex_unlock(struct pthread_mutex_t* mutex_t){ return 0; }
void pthread_cond_wait(struct pthread_cond_t* cond_t, struct pthread_mutex_t* mutex_t);
void pthread_cond_signal(struct pthread_cond_t* cond_t);
int main(int argc, char *argv[]) {
        const int MAX_LINE =  128;
	char file_name[25], output_file[] = "result.txt", line[MAX_LINE], *token,\
			result[100][40] = {{'0'}};
	const char delim[] = " .,;:!-\n\t";
	int freq[100] = {0}, i, n = 0, count = 0, num_lines = 0, tot_words = 0;
	if (argc > 1) {
		strcpy(file_name, argv[1]);
	} else {
		printf("What is the name of the file you are trying to access?\n");
		scanf("%s", file_name);
	}
        return 0; 
}
