#include "context.h"
void native_main_02058e28(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02029d5c((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
