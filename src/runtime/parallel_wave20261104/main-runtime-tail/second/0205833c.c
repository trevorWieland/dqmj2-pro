#include "context.h"
void native_main_0205833c(Context *context, const Instruction *instruction)
{
    int i = 0;
    do {
        context->parameters[i] = (float)native_fn_020d3e80(2, i);
        i++;
    } while (i < 6);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
