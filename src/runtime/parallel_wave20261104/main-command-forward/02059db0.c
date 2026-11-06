#include "context.h"
void native_main_02059db0(Context *context,const Instruction *instruction)
{
    Words4 current;
    native_fn_0200f3e0(&current);
    native_fn_020647a0(current.words[0],current.words[1],current.words[2]);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
