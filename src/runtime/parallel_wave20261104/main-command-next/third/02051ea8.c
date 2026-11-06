#include "context.h"
void native_main_02051ea8(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    u8 next;
    short last;
    float a = context->parameters[1];
    float b = context->parameters[2];
    float c = context->parameters[3];
    float d = context->parameters[4];
    next = (u32)context->parameters[5];
    last = (int)context->parameters[6];
    context->parameters[0] = (float)native_fn_ov000_02212c94(first,TO_FIXED(a),TO_FIXED(b),TO_FIXED(c),TO_FIXED(d),next,0,last);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
