#include "context.h"
void native_main_020581f8(Context *context, const Instruction *instruction)
{
    int i = 0;
    do {
        context->parameters[i] = (float)native_fn_020d3dc0(1, i);
        i++;
    } while (i < 3);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
