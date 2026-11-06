#include "context.h"
void native_main_0205a618(Context *context,const Instruction *instruction)
{
    native_fn_0205e6c4();
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
