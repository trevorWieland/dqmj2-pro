#include "context.h"
void native_main_020508ac(CommandContext *context, const Instruction *instruction)
{
    u16 first = (u32)context->parameters[0];
    NativeVec3 a,b,c,d;
    u8 last;
    a.x = TO_FIXED(context->parameters[1]);
    a.y = TO_FIXED(context->parameters[2]);
    a.z = TO_FIXED(context->parameters[3]);
    b.x = TO_FIXED(context->parameters[4]);
    b.y = TO_FIXED(context->parameters[5]);
    b.z = TO_FIXED(context->parameters[6]);
    c.x = TO_FIXED(context->parameters[7]);
    c.y = TO_FIXED(context->parameters[8]);
    c.z = TO_FIXED(context->parameters[9]);
    d.x = TO_FIXED(context->parameters[10]);
    d.y = TO_FIXED(context->parameters[11]);
    d.z = TO_FIXED(context->parameters[12]);
    last = (u32)context->parameters[13];
    native_fn_ov000_021e582c(first,&a,&b,&c,&d,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
