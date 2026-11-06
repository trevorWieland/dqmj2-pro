#include "context.h"
void native_main_0204d820(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    if(first>=0 && first<48)
        context->parameters[0]=(float)native_fn_ov000_0220a060(first);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
