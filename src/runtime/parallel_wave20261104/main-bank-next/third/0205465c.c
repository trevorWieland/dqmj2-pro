#include "context.h"
void native_main_0205465c(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_021e770c(instruction->payload);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
