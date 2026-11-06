#include "context.h"
void native_main_0204cbdc(Context *context,const Instruction *instruction)
{
    native_fn_020c5750((short)(int)context->parameters[0]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
