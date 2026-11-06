#include "context.h"
void native_main_0204e974(Context *context,const Instruction *instruction)
{
    Words3 words;
    int fourth;
    words.words[0]=TO_FIXED(context->parameters[0]);
    words.words[1]=TO_FIXED(context->parameters[1]);
    words.words[2]=TO_FIXED(context->parameters[2]);
    fourth=TO_FIXED(context->parameters[3]);
    native_fn_ov000_021e2ce8(&words,fourth);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
