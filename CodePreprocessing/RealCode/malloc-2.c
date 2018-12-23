#include <stdio.h>
typedef struct aeApiState {
    int epfd;
    char *events;
} aeApiState;
int aeApiCreate() {
    aeApiState *state = malloc(16);
    if (!state) return -1;
    if (!state->events) {
        free(state);
        state->events = malloc(8);
        return -1;
    }
}
