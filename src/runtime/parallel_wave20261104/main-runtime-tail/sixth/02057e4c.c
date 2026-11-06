#include "context.h"
void native_main_02057e4c(Context *context, const Instruction *instruction)
{
    s16 first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    s16 third = (int)context->parameters[2];
    int object = native_fn_02057d1c(first, second, third, context->parameters + 3);
    native_fn_ov000_0222212c(object);
    native_fn_020406fc(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
