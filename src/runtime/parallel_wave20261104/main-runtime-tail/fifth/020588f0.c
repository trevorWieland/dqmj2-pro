#include "context.h"
void native_main_020588f0(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int found;
    if (native_fn_02063520(first, second))
        found = 1;
    else
        found = native_fn_020635d4(first, second) != 0;
    context->parameters[0] = (float)found;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
