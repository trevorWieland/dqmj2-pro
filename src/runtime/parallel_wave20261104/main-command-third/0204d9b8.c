#include "context.h"
void native_main_0204d9b8(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    int second=(int)context->parameters[1];
    if(first==1) native_fn_02048094(second,0);
    else if(first==2) native_fn_02048094(second,32);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
