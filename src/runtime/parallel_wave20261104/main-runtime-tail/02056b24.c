#include "context.h"
void native_main_02056b24(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    context->parameters[0] = (float)native_fn_ov000_021e9738(first, second, third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
