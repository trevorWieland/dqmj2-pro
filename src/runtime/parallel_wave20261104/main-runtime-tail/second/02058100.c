#include "context.h"
void native_main_02058100(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205d8a4((u32)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
