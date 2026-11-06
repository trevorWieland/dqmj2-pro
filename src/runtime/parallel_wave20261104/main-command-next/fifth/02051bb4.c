#include "context.h"
void native_main_02051bb4(Context *context, const Instruction *instruction)
{
    int delta = (int)context->parameters[0];
    int value = native_fn_02062b0c();
    value = (int)((u32)value + (u32)delta);
    if (value > 999999) value = 999999;
    else if (value < 0) value = 0;
    native_fn_02062b1c(value);
    context->parameters[0] = (float)value;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
