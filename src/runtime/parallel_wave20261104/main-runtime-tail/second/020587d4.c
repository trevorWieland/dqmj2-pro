#include "context.h"
void native_main_020587d4(Context *context, const Instruction *instruction)
{
    native_fn_ov000_022094e8((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
