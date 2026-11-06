#include "context.h"
void native_main_0204eccc(Context *context,const Instruction *instruction)
{
    short first=(int)context->parameters[0];
    short second=(int)context->parameters[1];
    native_fn_ov000_021d8b10(native_fn_ov000_0221220c(first,second)+0x70);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
