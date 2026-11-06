#include "context.h"
void native_main_02054278(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = TO_FIXED(context->parameters[1]);
    native_fn_ov000_021e8e1c(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
