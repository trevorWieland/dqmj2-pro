#include "context.h"
void native_main_02051a14(Context *context, const Instruction *instruction)
{
    native_fn_020406ec(1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
