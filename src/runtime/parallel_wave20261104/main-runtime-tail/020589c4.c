#include "context.h"
void native_main_020589c4(Context *context, const Instruction *instruction)
{
    native_fn_0205e520();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
