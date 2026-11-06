#include "context.h"
void native_main_0204ca10(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    float value=context->parameters[1];
    int second=TO_FIXED(value);
    native_fn_ov000_021e8c80(first,second);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
