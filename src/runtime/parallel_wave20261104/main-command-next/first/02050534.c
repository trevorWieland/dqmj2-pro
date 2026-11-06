#include "context.h"
void native_main_02050534(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205f35c(-1,(int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
