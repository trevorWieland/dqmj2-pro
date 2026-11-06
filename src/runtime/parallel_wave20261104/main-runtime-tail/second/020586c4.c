#include "context.h"
void native_main_020586c4(Context *context, const Instruction *instruction)
{
    native_fn_ov000_022092e0(native_fn_ov000_02209244(instruction->payload));
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
