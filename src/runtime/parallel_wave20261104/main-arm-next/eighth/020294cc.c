#include "context.h"
u32 native_main_020294cc(RenderState *state)
{
    void *model;
    if (state->dirty0f) {
        Mtx33 xrotation;
        Mtx33 yrotation;
        Mtx33 zrotation;
        Mtx33 combined;
        native_fn_02000ce8(&combined);
        native_fn_020280a0(&zrotation, state->angles28.z);
        native_fn_02028044(&yrotation, state->angles28.y);
        native_fn_02027fe8(&xrotation, state->angles28.x);
        native_fn_02000e1c(&yrotation, &zrotation, &combined);
        native_fn_02000e1c(&xrotation, &combined, &state->matrix34);
        state->dirty0f = 0;
    }
    native_fn_02008d0c(&state->matrix34, &native_data_020ee04c);
    native_data_020edf90.flagsfc &= ~0xa4u;
    native_fn_0202e69c(&state->position10);
    native_fn_0202e6cc(&state->scale1c);
    native_fn_0202e66c();
    model = state->model08;
    native_fn_0202f5c8(model, 0, 0);
    native_fn_0202f730(model, 0, 0);
    native_fn_0202f6b8(model, 0, 1);
    native_fn_0202f7a8(model, 0, state->field0d);
    native_fn_0202f640(model, 0, 3);
    native_fn_0202dafc(model, 0, 0, 1);
    native_fn_0202f730(model, 0, 1);
    native_fn_0202f6b8(model, 0, 3);
    native_fn_0202dafc(model, 0, 0, 1);
    return 1;
}
