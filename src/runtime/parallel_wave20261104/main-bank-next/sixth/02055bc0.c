#include "context.h"
void native_main_02055bc0(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_021f3c48((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
