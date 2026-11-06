#include "context.h"
void native_main_020519cc(Context *context, const Instruction *instruction)
{
    native_fn_020406ec(0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
