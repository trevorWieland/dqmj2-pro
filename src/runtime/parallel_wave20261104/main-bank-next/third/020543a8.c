#include "context.h"
void native_main_020543a8(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02063d6c();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
