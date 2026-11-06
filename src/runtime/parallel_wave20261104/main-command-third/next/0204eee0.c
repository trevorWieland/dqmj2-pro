#include "context.h"
void native_main_0204eee0(ExtendedContext *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_02028158(native_fn_ov000_021d8a44()->field4c+0xb4000)/4096.0f;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
