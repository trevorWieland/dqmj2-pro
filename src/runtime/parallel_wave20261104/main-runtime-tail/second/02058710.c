#include "context.h"
void native_main_02058710(Context *context, const Instruction *instruction)
{
    native_fn_ov000_022092e0(native_fn_ov000_02209244(native_fn_0205dc70(2, 0, (u32)context->parameters[0])));
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
