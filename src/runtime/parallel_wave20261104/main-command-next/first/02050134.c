#include "context.h"
void native_main_02050134(Context *context, const Instruction *instruction)
{
    int index = (int)context->parameters[0];
    int value = TO_FIXED(context->parameters[1]);
    if (index >= 0 && index < 0x30)
        value = native_fn_ov000_02210b98(index,value);
    context->parameters[0] = (float)value / 4096.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
