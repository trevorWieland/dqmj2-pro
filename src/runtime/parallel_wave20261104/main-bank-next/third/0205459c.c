#include "context.h"
void native_main_0205459c(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    context->parameters[0] = (float)native_fn_ov000_021f3e28(first, second, 0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
