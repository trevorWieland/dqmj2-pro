#include "context.h"
void native_main_020583a8(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_020d38f0(native_fn_020d3738());
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
