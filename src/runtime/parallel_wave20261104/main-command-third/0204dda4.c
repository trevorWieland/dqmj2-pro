#include "context.h"
void native_main_0204dda4(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    int result;
    if(native_fn_02041bdc()==1) { native_fn_0204dd64(first); result=1; }
    else result=0;
    context->parameters[0]=(float)result;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
