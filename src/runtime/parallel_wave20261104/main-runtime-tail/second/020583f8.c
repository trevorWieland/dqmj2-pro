#include "context.h"
void native_main_020583f8(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_020d37f0();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
