#include "context.h"
void native_main_02056b9c(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int value = TO_FIXED(context->parameters[1]);
    native_fn_0205cea4(object, value);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
