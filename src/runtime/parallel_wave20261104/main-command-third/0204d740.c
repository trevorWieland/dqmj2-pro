#include "context.h"
void native_main_0204d740(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    u8 second=(u32)context->parameters[1];
    if(first>=0 && first<48)
        native_fn_ov000_02210344(first,second);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
