#include "context.h"
void native_main_02052600(Context *context, const Instruction *instruction)
{
    int third;
    int first = TO_FIXED(context->parameters[0]);
    int second = TO_FIXED(context->parameters[1]);
    u8 last;
    third = TO_FIXED(context->parameters[2]);
    last = (u32)context->parameters[3];
    native_fn_ov000_021e5ffc(first,second,third,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
