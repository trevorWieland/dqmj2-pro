#include "context.h"
void native_main_02057914(Context *context, const Instruction *instruction)
{
    s16 first = (int)context->parameters[0];
    s16 second = (int)context->parameters[1];
    AnimationObject *object = native_fn_ov000_0221220c(first, second);
    context->parameters[0] = (float)((object->second->descriptor->field4 << 12) - 1) / 4096.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
