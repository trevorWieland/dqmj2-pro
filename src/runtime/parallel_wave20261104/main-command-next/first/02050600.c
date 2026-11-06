#include "context.h"
void native_main_02050600(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    native_fn_0205f404(first,second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
