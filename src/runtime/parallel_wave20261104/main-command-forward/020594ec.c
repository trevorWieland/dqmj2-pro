#include "context.h"
void native_main_020594ec(Context *context,const Instruction *instruction)
{
    u32 value=(u32)context->parameters[0];
    native_fn_ov000_022096f4(instruction->payload,value);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
