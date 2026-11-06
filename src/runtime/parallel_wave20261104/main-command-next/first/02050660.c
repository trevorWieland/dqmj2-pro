#include "context.h"
void native_main_02050660(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    if (second < 0)
        second = 0;
    else if (second > 0x7f)
        second = 0x7f;
    native_fn_0205f6a0(first,second,third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
