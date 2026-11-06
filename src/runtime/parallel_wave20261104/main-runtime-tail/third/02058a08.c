#include "context.h"
void native_main_02058a08(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0203d1f0();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
