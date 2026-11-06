#include "context.h"
void native_main_02052420(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    int value = TO_FIXED(context->parameters[1]);
    u8 last;
    value = native_fn_02028158(value);
    last = (u32)context->parameters[2];
    native_fn_ov000_021e5c88(first,5,&value,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
