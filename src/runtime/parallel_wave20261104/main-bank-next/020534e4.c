#include "context.h"
void native_main_020534e4(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02229f68(1);
    native_fn_ov000_02229fdc(1);
    native_fn_ov000_0222a050(1);
    native_fn_ov000_0222a0c4(1);
    native_fn_ov000_0222a138(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
