#include "context.h"
void native_main_0204dccc(Context *context,const Instruction *instruction)
{
    native_fn_ov000_0221a0bc((int)context->parameters[0]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
