#include "context.h"
void native_main_020558ac(Context *context, const Instruction *instruction)
{
    int step = TO_FIXED(context->parameters[0]);
    int length = native_fn_ov000_021e71e0();
    Vec3 *first;
    Vec3 *second;
    Vec3 delta;
    if (length <= 0) {
        first = native_fn_0202859c(0, 0);
        second = native_fn_020285c8(0, 0);
        length = native_fn_0200285c(first, second);
    }
    native_fn_020284f4(0, step);
    first = native_fn_0202859c(0, 0);
    second = native_fn_020285c8(0, 0);
    delta.x = (int)((u32)first->x - (u32)second->x);
    delta.y = (int)((u32)first->y - (u32)second->y);
    delta.z = (int)((u32)first->z - (u32)second->z);
    native_fn_02002618(&delta, &delta);
    delta.x = FX_MUL(length, delta.x);
    delta.y = FX_MUL(length, delta.y);
    delta.z = FX_MUL(length, delta.z);
    first->x = (int)((u32)second->x + (u32)delta.x);
    first->y = (int)((u32)second->y + (u32)delta.y);
    first->z = (int)((u32)second->z + (u32)delta.z);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
