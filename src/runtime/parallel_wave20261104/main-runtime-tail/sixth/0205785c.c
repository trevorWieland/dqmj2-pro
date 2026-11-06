#include "context.h"
void native_main_0205785c(Context *context, const Instruction *instruction)
{
    s16 first = (int)context->parameters[0];
    s16 second = (int)context->parameters[1];
    int value = TO_FIXED(context->parameters[2]);
    AnimationObject *object = native_fn_ov000_0221220c(first, second);
    object->first->field0 = value;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
