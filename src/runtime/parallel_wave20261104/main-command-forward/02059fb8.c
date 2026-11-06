#include "context.h"
void native_main_02059fb8(Context *context,const Instruction *instruction)
{
    native_fn_020c3a30(0);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
