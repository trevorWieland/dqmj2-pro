#include "context.h"
void native_main_0204d884(ExtendedContext *context,const Instruction *instruction)
{
    native_fn_ov000_02219e40();
    native_fn_ov000_02219df8();
    native_fn_ov000_02219fbc(2);
    native_fn_ov000_02219fd8(1);
    native_fn_ov000_02219ff4(0);
    ORIGINAL_COMMAND_FLAG=1;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
