#include "context.h"
void native_main_02051cec(Context *context, const Instruction *instruction)
{
    if (native_fn_020820ac())
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
