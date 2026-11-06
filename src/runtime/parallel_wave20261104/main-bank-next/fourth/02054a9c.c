#include "context.h"
void native_main_02054a9c(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02063da8();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
