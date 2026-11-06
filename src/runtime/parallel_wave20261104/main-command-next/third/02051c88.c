#include "context.h"
void native_main_02051c88(Context *context, const Instruction *instruction)
{
    if (native_fn_02081fc8((int)context->parameters[0],1))
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
