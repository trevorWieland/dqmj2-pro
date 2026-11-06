#include "context.h"
void native_main_020598e8(Context *context,const Instruction *instruction)
{
    native_fn_02064754(*native_fn_020633bc());
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
