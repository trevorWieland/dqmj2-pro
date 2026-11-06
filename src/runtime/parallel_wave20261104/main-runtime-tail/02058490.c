#include "context.h"
void native_main_02058490(Context *context, const Instruction *instruction)
{
    native_fn_ov000_02208dcc();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
