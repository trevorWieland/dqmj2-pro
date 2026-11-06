#include "context.h"
int native_main_02028dcc(Flags *state)
{
    if (state->flagc) {
        state->flagc = 0;
        return 1;
    }
    return 0;
}
