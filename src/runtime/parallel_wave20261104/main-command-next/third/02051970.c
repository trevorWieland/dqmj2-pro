#include "context.h"
void native_main_02051970(Context *context, const Instruction *instruction)
{
    u8 value = (u32)context->parameters[0];
    native_fn_0205be34(value);
    native_fn_0204040c(value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
