#include "context.h"
void native_main_020574dc(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_02214a54();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
