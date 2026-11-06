#include "context.h"
void native_main_02056c34(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_0205d718((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
