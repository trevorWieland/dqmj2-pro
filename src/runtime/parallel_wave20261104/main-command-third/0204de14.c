#include "context.h"
void native_main_0204de14(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_ov000_021e0d78((int)context->parameters[0],0,1);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
