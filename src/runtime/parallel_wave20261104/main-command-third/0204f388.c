#include "context.h"
void native_main_0204f388(Context *context,const Instruction *instruction)
{
    native_fn_ov000_021d8c80(1);
    native_fn_ov000_021d8a08(0);
    native_fn_ov000_021d8a28();
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
