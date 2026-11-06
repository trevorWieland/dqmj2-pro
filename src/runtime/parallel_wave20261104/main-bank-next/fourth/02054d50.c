#include "context.h"
void native_main_02054d50(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    u16 value = (u32)context->parameters[1];
    u32 handle = native_fn_020725e8(object);
    native_fn_ov007_021d8754(handle, value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
