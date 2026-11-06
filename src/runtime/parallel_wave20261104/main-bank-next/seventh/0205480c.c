#include "context.h"
void native_main_0205480c(Context *context, const Instruction *instruction, int selector)
{
    int value = (int)context->parameters[0];
    int mask;
    u32 bits;
    int result;
    if (value == 0)
        mask = 0;
    else if (value == 3)
        mask = 63;
    else if (value == 1)
        mask = 57;
    else
        mask = 62;
    if (selector == 0)
        bits = native_fn_020414b0(mask);
    else
        bits = native_fn_020414c8(mask);
    if ((bits & 1) && (bits & 2))
        result = 3;
    else if (bits & 1)
        result = 1;
    else if (bits & 2)
        result = 2;
    else
        result = 0;
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
