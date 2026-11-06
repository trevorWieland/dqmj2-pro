#include "context.h"
void native_main_0204e27c(Context *context,const Instruction *instruction)
{
    native_fn_0205e3c0((short)(int)context->parameters[0]);
    native_fn_020404f0(19);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
