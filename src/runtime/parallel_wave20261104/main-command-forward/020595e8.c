#include "context.h"
void native_main_020595e8(Context *context,const Instruction *instruction)
{
    native_fn_0203d294(0);
    native_fn_020c58f8(0);
    native_fn_020c5948(0);
    native_fn_020443d4(6);
    native_fn_02064978();
    native_fn_02044454(70);
    native_fn_020652dc((int)context->parameters[0]);
    native_fn_02065304(0);
    native_fn_02065630(0);
    native_fn_02065648((u32)context->parameters[1]);
    native_fn_0206532c(3);
    native_fn_0206534c(-1);
    native_fn_020652c4(0);
    native_fn_0205bd60()[12]=1;
    native_fn_020656d0(1);
    native_fn_020656b0(1);
    native_fn_020404f0(26);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
