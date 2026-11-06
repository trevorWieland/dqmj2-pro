#include "context.h"
void native_main_020507b0(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    if (first < 0) first = 0;
    else if (first > 127) first = 127;
    native_fn_0205f6a0(0,first,second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
