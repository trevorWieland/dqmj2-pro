#include "context.h"
void native_main_0204cc30(Context *context,const Instruction *instruction)
{
    native_fn_ov000_0220a078(native_fn_020c56b4((int)context->parameters[0])->field2+0x34);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
