#include "context.h"
void native_main_0205903c(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_021e632c(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
