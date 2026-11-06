#include "context.h"
void native_main_0204e914(Context *context,const Instruction *instruction)
{
    u32 first=(u32)context->parameters[0];
    u8 second=(u32)context->parameters[1];
    native_fn_0205c218(first,second);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
