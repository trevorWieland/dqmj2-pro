#include "context.h"
void native_main_02053fb8(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02063cf4();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
