#include "context.h"
void native_main_02051dac(Context *context, const Instruction *instruction)
{
    if (native_fn_020823f4())
        context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
