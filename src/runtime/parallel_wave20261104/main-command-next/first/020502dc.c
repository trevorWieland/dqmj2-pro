#include "context.h"
void native_main_020502dc(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_ov000_021e7b9c((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
