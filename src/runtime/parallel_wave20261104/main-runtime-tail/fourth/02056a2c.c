#include "context.h"
void native_main_02056a2c(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int value = TO_FIXED(context->parameters[1]);
    context->parameters[0] = (float)native_fn_0205ccb8(object, value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
