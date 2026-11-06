#include "context.h"
void native_main_0205860c(Context *context, const Instruction *instruction)
{
    s16 first = (int)context->parameters[0];
    s16 second = (int)context->parameters[1];
    native_fn_ov000_0220925c(first, second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
