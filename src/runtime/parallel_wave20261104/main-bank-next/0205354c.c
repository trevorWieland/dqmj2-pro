#include "context.h"
void native_main_0205354c(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02229fb0(1);
    native_fn_ov000_0222a024(1);
    native_fn_ov000_0222a098(1);
    native_fn_ov000_0222a10c(1);
    native_fn_ov000_0222a17c(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
