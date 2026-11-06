#include "context.h"
void native_main_020549d4(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    context->parameters[0] = (float)native_fn_0203d0d8(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
