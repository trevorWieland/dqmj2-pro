#include "context.h"
void native_main_0204b4f4(LayoutState *state, const Point *point, u32 step, u32 argument3, u32 argument4, u8 argument5)
{
    native_fn_0204b1c4(state, 0, point, argument3, argument4, argument5);
    state->step = step;
    native_fn_0204b53c(state, point);
}
