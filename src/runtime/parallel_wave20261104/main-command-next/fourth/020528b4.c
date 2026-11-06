#include "context.h"
void native_main_020528b4(Context *context, const Instruction *instruction)
{
    native_fn_0206344c();
    native_fn_0206349c();
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
