#include "context.h"
void native_main_0204e568(Context *context,const Instruction *instruction)
{
    short first=(int)context->parameters[0];
    short second=(int)context->parameters[1];
    native_fn_0204b818(first,second);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
