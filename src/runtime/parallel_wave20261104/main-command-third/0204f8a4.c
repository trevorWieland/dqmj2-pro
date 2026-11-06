#include "context.h"
void native_main_0204f8a4(Context *context,const Instruction *instruction)
{
    native_fn_020404f0(36);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
