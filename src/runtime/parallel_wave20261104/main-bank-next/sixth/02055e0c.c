#include "context.h"
void native_main_02055e0c(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    float first = context->parameters[1];
    float second = context->parameters[2];
    float third = context->parameters[3];
    native_fn_ov000_021f3f88(object, TO_FIXED(first), TO_FIXED(second), TO_FIXED(third));
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
