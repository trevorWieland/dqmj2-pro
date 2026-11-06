#include "context.h"
void native_main_02056acc(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_021e31f0((int)context->parameters[0], 0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
