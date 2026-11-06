#include "context.h"
void native_main_0204b74c(LayoutState *state, u32 step)
{
    Point point;
    state->step = step;
    point.x = state->position.x;
    point.y = state->position.y;
    native_fn_0204b6dc(state, &point);
}
