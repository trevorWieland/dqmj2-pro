#include "context.h"
void native_main_0204e1c8(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_ov000_021e5594((int)context->parameters[0]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
