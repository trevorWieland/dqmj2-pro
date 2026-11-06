#include "context.h"
void native_main_02054918(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    u8 second = (u32)context->parameters[1];
    context->parameters[0] = (float)native_fn_0203d0c0(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
