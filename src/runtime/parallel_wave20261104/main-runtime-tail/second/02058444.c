#include "context.h"
void native_main_02058444(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205c278();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
