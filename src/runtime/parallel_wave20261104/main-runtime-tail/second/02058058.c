#include "context.h"
void native_main_02058058(Context *context, const Instruction *instruction)
{
    native_fn_02040534(1U << (u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
