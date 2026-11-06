#include "context.h"
void native_main_02058000(Context *context, const Instruction *instruction)
{
    if (native_fn_0205e844((int)context->parameters[0]))
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
