#include "context.h"
void native_main_020580ac(Context *context, const Instruction *instruction)
{
    native_fn_02040518(1U << (u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
