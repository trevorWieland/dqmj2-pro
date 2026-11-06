#include "context.h"
void native_main_0204b380(LayoutState *state, int enabled)
{
    u8 index;
    FieldObject *last;
    if (!state->group) return;
    index = 0;
    do {
        FieldObject *object = native_fn_0205f98c(state->group, index);
        if (enabled) object->field7c |= 2;
        else object->field7c &= ~2u;
        ++index;
    } while (index < 2);
    last = native_fn_0205f98c(state->group, 2);
    if (enabled) {
        if (!native_fn_0204b4b8(state)) return;
        last->field7c |= 2;
    } else last->field7c &= ~2u;
}
