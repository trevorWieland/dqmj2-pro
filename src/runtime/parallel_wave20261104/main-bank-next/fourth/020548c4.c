#include "context.h"
void native_main_020548c4(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)(u32)native_fn_0203d0b4((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
