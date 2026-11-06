#include "context.h"
void native_main_02052840(Context *context, const Instruction *instruction)
{
    int value = (int)context->parameters[0];
    int magnitude = value < 0 ? -value : value;
    int result;
    if (magnitude) {
        result = native_fn_0203d294(magnitude);
        if (value < 0) result = -result;
    } else result = 0;
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
