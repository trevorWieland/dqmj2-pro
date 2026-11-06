#include "context.h"
void native_main_02059388(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int first = TO_FIXED(context->parameters[1]);
    int second = TO_FIXED(context->parameters[2]);
    int third = TO_FIXED(context->parameters[3]);
    int fourth = TO_FIXED(context->parameters[4]);
    native_fn_0205eb0c(object, first, second, third, fourth);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
