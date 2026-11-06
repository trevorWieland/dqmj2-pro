#include "context.h"
void native_main_02056628(Context *context, const Instruction *instruction)
{
    native_fn_ov000_021e71a4(0, TO_FIXED(context->parameters[0]));
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
