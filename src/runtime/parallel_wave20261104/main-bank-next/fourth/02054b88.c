#include "context.h"
void native_main_02054b88(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    u8 data[4];
    u32 handle;
    data[0] = (u32)context->parameters[1];
    data[1] = (u32)context->parameters[2];
    data[2] = (u32)context->parameters[3];
    data[3] = (u32)context->parameters[4];
    handle = native_fn_020725e8(object);
    native_fn_020c1fdc(handle, data);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
