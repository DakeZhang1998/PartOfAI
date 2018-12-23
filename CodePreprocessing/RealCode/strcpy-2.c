#include <stdio.h>
int main(int argc, char *argv[]) {
        const int MAX_LINE =  128;
	char file_name[25], output_file[] = "result.txt", line[MAX_LINE], *token,\
			result[100][40] = {{'0'}};
	const char delim[] = " .,;:!-\n\t";
	int freq[100] = {0}, i, n = 0, count = 0, num_lines = 0, tot_words = 0;
	FILE *myFile, *result_file;
	if (argc > 1) {
		strncpy(file_name, argv[1],sizeof(file_name));
	} else {
		printf("What is the name of the file you are trying to access?\n");
		scanf("%s", file_name);
	}
        return 0; 
}
