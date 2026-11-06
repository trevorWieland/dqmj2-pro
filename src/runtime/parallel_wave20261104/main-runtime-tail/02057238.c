#include "context.h"
void native_main_02057238(Context *context, const Instruction *instruction)
{
    native_fn_02040820();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 1;
}
