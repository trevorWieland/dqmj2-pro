#include "context.h"
void native_main_02054700(Context *context, const Instruction *instruction, int selector)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    if (selector == 0)
        native_fn_02041510(first, second, third);
    else
        native_fn_02041538(first, second, third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
