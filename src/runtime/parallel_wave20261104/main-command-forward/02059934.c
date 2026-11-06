#include "context.h"
void native_main_02059934(Context *context,const Instruction *instruction)
{
    u32 first=*native_fn_020633bc();
    u32 second=native_fn_0206476c();
    u32 result=second>=first?0:(first-second)/1800;
    context->parameters[0]=(float)result;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
