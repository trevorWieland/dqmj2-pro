#include "context.h"
void native_main_0204ee50(ExtendedContext *context,const Instruction *instruction,u32 third)
{
    native_fn_ov000_021d84e8(TO_FIXED(context->parameters[0])+0xb4000,third);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
