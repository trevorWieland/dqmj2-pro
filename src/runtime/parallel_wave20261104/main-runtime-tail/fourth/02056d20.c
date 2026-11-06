#include "context.h"
void native_main_02056d20(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int first = TO_FIXED(context->parameters[1]);
    int second = TO_FIXED(context->parameters[2]);
    int third = TO_FIXED(context->parameters[3]);
    int coordinates[3];
    native_fn_0205cdf0(object, coordinates);
    native_fn_0205cda8(object, first + coordinates[0], second + coordinates[1], third + coordinates[2]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
