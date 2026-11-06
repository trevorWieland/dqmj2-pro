#include "context.h"
void native_main_020596b8(Context *context,const Instruction *instruction)
{
    context->parameters[0]=(float)native_fn_02064454();
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
