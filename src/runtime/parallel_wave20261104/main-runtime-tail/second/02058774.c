#include "context.h"
void native_main_02058774(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    int second = (int)context->parameters[1];
    native_fn_ov000_022093ec(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
