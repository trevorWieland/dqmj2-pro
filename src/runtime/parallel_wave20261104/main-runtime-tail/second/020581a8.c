#include "context.h"
void native_main_020581a8(Context *context, const Instruction *instruction)
{
    native_fn_020d3fbc((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
