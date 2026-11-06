#include "context.h"
void native_main_020599f8(Context *context,const Instruction *instruction)
{
    int value=(int)context->parameters[0];
    int *slot=native_fn_02065d88(234);
    int previous=*slot;
    *slot=value;
    context->parameters[0]=(float)previous;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
