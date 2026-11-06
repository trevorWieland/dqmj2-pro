#include "context.h"
void native_main_02059e20(Context *context,const Instruction *instruction)
{
    const PackedFields4 *saved=native_fn_020647b8();
    Words4 current;
    native_fn_0200f3e0(&current);
    if(saved->field3!=current.words[2]) {
        context->parameters[0]=1.0f;
        END_COMMAND(0);
    }
    if(saved->field2!=current.words[1]) {
        context->parameters[0]=1.0f;
        END_COMMAND(0);
    }
    if(saved->field0!=current.words[0]) {
        context->parameters[0]=1.0f;
        END_COMMAND(0);
    }
    context->parameters[0]=0.0f;
    END_COMMAND(0);
}
