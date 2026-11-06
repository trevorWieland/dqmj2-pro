#include "context.h"
void native_main_02057434(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    u8 second = (u32)context->parameters[1];
    u8 third = (u32)context->parameters[2];
    native_fn_02029c88(first, second, third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
