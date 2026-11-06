#include "context.h"
void native_main_02051afc(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    signed char second = (int)context->parameters[1];
    context->parameters[0] = (float)native_fn_020630e4(first,second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
