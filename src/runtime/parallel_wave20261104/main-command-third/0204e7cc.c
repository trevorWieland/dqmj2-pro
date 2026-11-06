#include "context.h"
void native_main_0204e7cc(Context *context,const Instruction *instruction)
{
    native_fn_ov000_021e0b88(TO_FIXED(context->parameters[0]));
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
