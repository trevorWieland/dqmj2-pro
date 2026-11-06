#include "context.h"
void native_main_02051b68(Context *context, const Instruction *instruction)
{
    context->parameters[0] = (float)native_fn_02062b0c();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
