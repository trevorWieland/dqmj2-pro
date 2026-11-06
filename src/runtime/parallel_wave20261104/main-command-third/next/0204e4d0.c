#include "context.h"
void native_main_0204e4d0(ExtendedContext *context,const Instruction *instruction)
{
    native_fn_0205bf2c(2);
    native_fn_0205bdfc(native_fn_ov000_021df1f0());
    native_fn_0205bf04(0);
    native_fn_0205be4c(-1);
    native_fn_0205be74(native_fn_ov000_021e07b8(0));
    native_fn_0205bea4(native_fn_ov000_021e07d4(0)->words[1]);
    native_fn_0205bed4(native_fn_ov000_021d8a44()->field98);
    native_fn_0205c020(2);
    native_fn_020404f0(31);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
