#include "context.h"
void native_main_020504cc(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    if (first >= 0)
        native_fn_ov000_021e7bb0(first,second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
