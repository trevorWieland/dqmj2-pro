#include "context.h"
void native_main_02057c4c(Context *context, const Instruction *instruction)
{
    u16 first = (u32)context->parameters[0];
    int second = (int)context->parameters[1];
    native_fn_ov000_02218d20(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
