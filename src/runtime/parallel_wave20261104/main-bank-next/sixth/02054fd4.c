#include "context.h"
void native_main_02054fd4(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205be24();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
