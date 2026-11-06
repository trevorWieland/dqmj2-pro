#include "context.h"
void native_main_02054784(Context *context, const Instruction *instruction, int selector)
{
    if (selector == 0) {
        if (native_fn_02041800() != 1)
            context->records[context->bank].position += instruction->advance;
    } else {
        if (native_fn_02041814() != 1)
            context->records[context->bank].position += instruction->advance;
    }
    context->records[context->bank].status = 1;
}
