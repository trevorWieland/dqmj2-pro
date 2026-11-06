#include "context.h"
void native_main_02050828(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    if (second < 0) second = 0;
    else if (second > 127) second = 127;
    native_fn_0205f7e0(first,second,third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
