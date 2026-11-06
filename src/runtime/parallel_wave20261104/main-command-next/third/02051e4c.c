#include "context.h"
void native_main_02051e4c(Context *context, const Instruction *instruction)
{
    int value = (int)context->parameters[0];
    if (value < 18)
        context->parameters[0] = (float)native_fn_ov000_022129f8(value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
