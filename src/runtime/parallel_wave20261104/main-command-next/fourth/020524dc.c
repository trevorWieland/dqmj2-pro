#include "context.h"
void native_main_020524dc(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    int value[2] = {(int)context->parameters[1],(int)context->parameters[2]};
    u8 last = (u32)context->parameters[3];
    native_fn_ov000_021e5c88(first,6,value,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
