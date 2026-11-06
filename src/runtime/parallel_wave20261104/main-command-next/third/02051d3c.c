#include "context.h"
void native_main_02051d3c(Context *context, const Instruction *instruction)
{
    if (native_fn_02081fc8((int)context->parameters[0],0))
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
