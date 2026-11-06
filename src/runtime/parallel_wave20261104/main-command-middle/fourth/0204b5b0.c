#include "context.h"
void native_main_0204b5b0(LayoutState *state, u32 step)
{
    Point point;
    state->step = step;
    point.x = state->position.x;
    point.y = state->position.y;
    native_fn_0204b53c(state, &point);
}
