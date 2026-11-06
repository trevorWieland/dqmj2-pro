#include "context.h"
void native_main_02059704(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_020c5938();
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
