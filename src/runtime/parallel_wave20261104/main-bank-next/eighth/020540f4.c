#include "context.h"
void native_main_020540f4(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    const Vec3 *point = native_fn_ov000_021e07b8(0);
    native_fn_ov000_021e8de8(object, point->x, point->y, point->z);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
