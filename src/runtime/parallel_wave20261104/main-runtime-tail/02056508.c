#include "context.h"
void native_main_02056508(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int first = TO_FIXED(context->parameters[1]);
    int second = TO_FIXED(context->parameters[2]);
    int third = TO_FIXED(context->parameters[3]);
    native_fn_ov000_021f3fec(object, first, second, third);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
