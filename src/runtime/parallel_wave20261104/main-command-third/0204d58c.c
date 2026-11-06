#include "context.h"
void native_main_0204d58c(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    int second=TO_FIXED(context->parameters[1]);
    if(first>=0 && first<48)
        native_fn_ov000_02210f20(first,second,1);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
