#include "context.h"
void native_main_02050590(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    native_fn_0205f4bc(first,second,third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
