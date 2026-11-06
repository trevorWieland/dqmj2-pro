#include "context.h"
void native_main_02057324(Context *context, const Instruction *instruction)
{
    if (native_fn_ov000_021e9794((int)context->parameters[0]))
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
