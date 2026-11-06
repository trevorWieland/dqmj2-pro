#include "context.h"
void native_main_02051aa8(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02063144((int)context->parameters[0]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
