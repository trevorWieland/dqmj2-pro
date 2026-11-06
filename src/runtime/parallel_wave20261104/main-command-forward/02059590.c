#include "context.h"
void native_main_02059590(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)(native_fn_02027400()==9);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
