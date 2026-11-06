#include "context.h"
void native_main_020584d4(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    u8 second = (u32)context->parameters[1];
    int third = (int)context->parameters[2];
    int fourth = (int)context->parameters[3];
    int fifth = (int)context->parameters[4];
    int sixth = (int)context->parameters[5];
    native_fn_ov000_0220913c(first, second, third, fourth, fifth, sixth);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
