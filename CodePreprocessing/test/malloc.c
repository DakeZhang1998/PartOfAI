#include <stdio.h>
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
