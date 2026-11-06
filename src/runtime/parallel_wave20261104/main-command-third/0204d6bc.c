#include "context.h"
void native_main_0204d6bc(Context *context,const Instruction *instruction)
{
    u32 result=0;
    int first=(int)context->parameters[0];
    u8 second=(u32)context->parameters[1];
    if(first>=0 && first<48)
        result=native_fn_ov000_022108dc(first,second);
    context->parameters[0]=(float)result;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
