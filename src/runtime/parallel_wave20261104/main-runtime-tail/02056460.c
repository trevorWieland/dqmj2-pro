#include "context.h"
void native_main_02056460(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int fixed = TO_FIXED(context->parameters[1]);
    context->parameters[0] = (float)native_fn_ov000_021f3ec4(object, fixed) / 4096.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
