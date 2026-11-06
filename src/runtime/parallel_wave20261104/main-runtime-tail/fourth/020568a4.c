#include "context.h"
void native_main_020568a4(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int first = TO_FIXED(context->parameters[1]);
    int second = TO_FIXED(context->parameters[2]);
    int third = TO_FIXED(context->parameters[3]);
    int fourth = TO_FIXED(context->parameters[4]);
    u8 flag = (u32)context->parameters[5];
    context->parameters[0] = (float)native_fn_ov000_021e970c(object, first, second, third, fourth, flag);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
