#include "context.h"
void native_main_020572cc(Context *context, const Instruction *instruction)
{
    u8 value = (u32)context->parameters[0];
    native_fn_ov000_021e9e4c(value, 16 - value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
