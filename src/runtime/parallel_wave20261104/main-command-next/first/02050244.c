#include "context.h"
void native_main_02050244(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02040424();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
