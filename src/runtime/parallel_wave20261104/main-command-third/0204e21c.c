#include "context.h"
void native_main_0204e21c(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    u8 second=(u32)context->parameters[1];
    native_fn_ov000_021e577c(first,second);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
