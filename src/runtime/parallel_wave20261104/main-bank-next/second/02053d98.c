#include "context.h"
void native_main_02053d98(Context *context, const Instruction *instruction)
{
    native_fn_0204077c();
    native_fn_0204073c(0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
