#include "context.h"
void native_main_020567c0(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205c668((int)context->parameters[0], 1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
