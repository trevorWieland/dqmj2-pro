#include "context.h"
void native_main_02057574(Context *context, const Instruction *instruction)
{
    u8 mode = (u32)context->parameters[0];
    native_fn_0203d0e4(mode);
    if (mode == 1)
        native_fn_ov000_0222a24c(1);
    else if (mode == 2)
        native_fn_ov000_0222a24c(2);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
