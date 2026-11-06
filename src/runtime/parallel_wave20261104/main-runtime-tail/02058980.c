#include "context.h"
void native_main_02058980(Context *context, const Instruction *instruction)
{
    native_fn_0205e61c();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
