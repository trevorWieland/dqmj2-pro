#include "context.h"
void native_main_020561a0(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    float value = context->parameters[1];
    context->parameters[0] = (float)native_fn_ov000_021f4208(object, TO_FIXED(value)) / 4096.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
