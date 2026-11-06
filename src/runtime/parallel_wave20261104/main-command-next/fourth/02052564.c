#include "context.h"
void native_main_02052564(Context *context, const Instruction *instruction)
{
    u8 first = (u32)context->parameters[0];
    float value = context->parameters[1];
    native_fn_ov000_021e5ec0(first,TO_FIXED(value));
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
