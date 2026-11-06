#include "context.h"
void native_main_0204f3dc(Context *context,const Instruction *instruction)
{
    native_fn_ov000_021d8a08((int)context->parameters[0]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
