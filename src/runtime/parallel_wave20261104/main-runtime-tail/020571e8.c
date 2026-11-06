#include "context.h"
void native_main_020571e8(Context *context, const Instruction *instruction)
{
    native_fn_0205e3f0((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
