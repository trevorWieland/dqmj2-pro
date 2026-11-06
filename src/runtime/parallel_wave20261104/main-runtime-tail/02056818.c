#include "context.h"
void native_main_02056818(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    signed char third = (int)context->parameters[2];
    int fourth = (int)context->parameters[3];
    context->parameters[0] = (float)native_fn_ov000_021e96cc(first, second, third, fourth);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
