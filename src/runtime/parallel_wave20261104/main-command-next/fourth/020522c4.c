#include "context.h"
void native_main_020522c4(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    int value = (int)context->parameters[1];
    u8 last = (u32)context->parameters[2];
    native_fn_ov000_021e5c88(first,1,&value,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
