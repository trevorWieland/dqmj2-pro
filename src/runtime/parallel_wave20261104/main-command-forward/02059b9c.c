#include "context.h"
void native_main_02059b9c(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_02063f04((int)context->parameters[0])->field10;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
