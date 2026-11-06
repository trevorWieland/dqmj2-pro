#include "context.h"
void native_main_0205006c(Context *context, const Instruction *instruction)
{
    signed char first = (int)context->parameters[0];
    short second = (int)context->parameters[1];
    native_fn_0205bd6c(0,0,0,0,0,0,second,1,0,0,0,first,0x2d,1,0,0,0,0);
    native_fn_ov000_021e7940(0);
    native_fn_020404f0(0x1b);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
