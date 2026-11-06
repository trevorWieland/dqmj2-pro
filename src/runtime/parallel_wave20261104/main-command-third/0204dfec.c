#include "context.h"
void native_main_0204dfec(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_ov000_02213cdc((int)context->parameters[0]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
