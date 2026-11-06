#include "context.h"
void native_main_02058cd0(Context *context, const Instruction *instruction)
{
    int first = TO_FIXED(context->parameters[0]);
    int second = TO_FIXED(context->parameters[1]);
    first = native_fn_ov000_021f4280(first);
    second = native_fn_ov000_021f4298(second);
    context->parameters[0] = (float)first / 4096.0f;
    context->parameters[1] = (float)second / 4096.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
