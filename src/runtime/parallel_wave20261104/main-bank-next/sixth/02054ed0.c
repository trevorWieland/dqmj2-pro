#include "context.h"
void native_main_02054ed0(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    u32 second = (u32)context->parameters[1];
    native_fn_020725c8(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
