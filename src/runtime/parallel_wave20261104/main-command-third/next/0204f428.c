#include "context.h"
void native_main_0204f428(ExtendedContext *context,const Instruction *instruction)
{
    u8 kind=(u32)context->parameters[0];
    Words3 words;
    int fourth;
    words.words[0]=TO_FIXED(context->parameters[1]);
    words.words[1]=TO_FIXED(context->parameters[2]);
    words.words[2]=TO_FIXED(context->parameters[3]);
    fourth=TO_FIXED(context->parameters[4]);
    native_fn_0205c2d4(kind);
    native_fn_0205c2b4(&words);
    native_fn_0205c2f4(fourth);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
