#include "context.h"
void native_main_02055c14(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int result = native_fn_ov000_021f3c48(first);
    if (result >= 0)
        native_fn_ov000_021f3dac(result, second);
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
