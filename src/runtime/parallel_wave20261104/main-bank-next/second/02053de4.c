#include "context.h"
void native_main_02053de4(Context *context, const Instruction *instruction)
{
    native_fn_0204073c(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
