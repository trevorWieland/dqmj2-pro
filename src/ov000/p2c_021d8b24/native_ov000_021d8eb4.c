#include "context.h"

/* Refresh the renderer's cached copy of the two input vectors, publish the
   distance between them, and hand the new position to the scene updater. The
   live/previous vector mirrors are only refreshed when `flag` asks for it. */
void native_ov000_021d8eb4(Vec3 *first, Vec3 *second, s32 flag, s32 mode)
{
    s32 distance;
    StateBlock *block = native_fn_ov000_021d8a44();

    if (flag != 0) {
        block->field_8c = *first;
        block->field_80 = *second;
    }
    distance = native_fn_0202818c(first, second);
    if (flag != 0) {
        block->field_5c = *second;
        block->field_1c = *second;
        block->field_68 = *first;
        block->field_28 = *first;
        block->field_74 = *second;
    }
    native_fn_ov000_021d8ae8(first);
    native_fn_ov000_021d8a44()->field_a0 = second->y - first->y;
    first->y = 0;
    second->y = 0;
    native_fn_ov000_021d8a44()->field_9c = native_fn_0200285c(second, first);
    native_fn_ov000_021d8a44()->field_a4 = 0;
    native_fn_ov000_021d84e8(distance);
    if (flag != 0)
        block->field_50 = native_fn_ov000_021d8a44()->field_9c;
    block->field_54 = native_fn_ov000_021d8a44()->field_a0;
    block->field_58 = native_fn_ov000_021d8a44()->field_a4;
    if (flag != 0)
        block->field_4c = block->field_98;
    native_fn_ov000_021d8a08(mode);
}
