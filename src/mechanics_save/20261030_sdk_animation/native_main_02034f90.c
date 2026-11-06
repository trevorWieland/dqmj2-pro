#include "animation_types_v2.h"
extern u32 native_fn_02034d68(AnimationControl *control, s32 delta);
void native_main_02034f90(AnimationControl *control) {
    u32 forward;
    forward = control->speed > 0;
    if ((forward ^ control->reverse) != 0) {
        control->frame = control->sequence->frames + control->sequence->loopStart;
    } else {
        control->frame = control->sequence->frames + control->sequence->count - 1;
    }
    control->active = control->frame;
    control->elapsed = 0;
    native_fn_02034d68(control, 0);
}
