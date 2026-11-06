#include "context.h"
void native_main_0204e480(Context *context,const Instruction *instruction)
{
    native_fn_ov000_02219404((u32)context->parameters[0]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
