#include "context.h"
void native_main_0204e2d8(Context *context,const Instruction *instruction)
{
    u8 kind=(u32)context->parameters[0];
    int first=TO_FIXED(context->parameters[1]);
    int second=TO_FIXED(context->parameters[2]);
    int third=TO_FIXED(context->parameters[3]);
    int fourth=TO_FIXED(context->parameters[4]);
    Words3 words;
    words.words[0]=first;
    words.words[1]=second;
    words.words[2]=third;
    native_fn_0205bf2c(2);
    native_fn_0205bdfc(kind);
    native_fn_0205bf04(0);
    native_fn_0205be4c(-1);
    native_fn_0205be74(&words);
    native_fn_0205bea4(fourth);
    native_fn_0205bed4(native_fn_ov000_021d8a44()->field98);
    native_fn_020404f0(31);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
