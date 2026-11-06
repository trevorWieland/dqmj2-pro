#include "context.h"
void native_main_02057528(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_02214acc();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
