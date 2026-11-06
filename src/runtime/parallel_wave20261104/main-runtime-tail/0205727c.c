#include "context.h"
void native_main_0205727c(Context *context, const Instruction *instruction)
{
    native_fn_ov000_021e9df4((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
