#include "context.h"
void native_main_020503d0(Context *context, const Instruction *instruction)
{
    int value = (int)context->parameters[0];
    if (value > 0)
        native_fn_ov000_021e7940(value);
    else
        native_fn_ov000_021e7940(0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
