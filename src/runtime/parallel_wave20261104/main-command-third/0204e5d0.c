#include "context.h"
void native_main_0204e5d0(Context *context,const Instruction *instruction)
{
    native_fn_0204b79c();
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
