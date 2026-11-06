#include "context.h"
void native_main_02050f4c(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    native_fn_ov000_022124b4(first,second,third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
