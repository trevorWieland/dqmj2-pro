#include "context.h"
void native_main_0204df90(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    native_fn_02047d40(first);
    context->parameters[0]=(float)first;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
