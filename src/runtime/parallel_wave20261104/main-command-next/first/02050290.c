#include "context.h"
void native_main_02050290(Context *context, const Instruction *instruction)
{
    native_fn_0205e73c((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
