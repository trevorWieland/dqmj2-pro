#include "context.h"
void native_main_02052340(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    int value = (int)context->parameters[1] * 30;
    u8 last = (int)context->parameters[2];
    native_fn_ov000_021e5c88(first,2,&value,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
