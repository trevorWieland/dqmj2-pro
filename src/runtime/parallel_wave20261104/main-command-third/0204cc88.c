#include "context.h"
void native_main_0204cc88(Context *context,const Instruction *instruction)
{
    native_fn_ov000_02210908(native_fn_020c56b4((int)context->parameters[0])->field2+0x34);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
