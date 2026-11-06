#include "context.h"
void native_main_020523c4(Context *context, const Instruction *instruction)
{
    native_fn_ov000_021e5c88((u32)context->parameters[0],3,0,0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
