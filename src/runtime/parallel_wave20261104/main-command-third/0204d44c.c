#include "context.h"
void native_main_0204d44c(Context *context,const Instruction *instruction)
{
    int first=(int)context->parameters[0];
    Words3 words;
    words.words[0]=TO_FIXED(context->parameters[1]);
    words.words[1]=TO_FIXED(context->parameters[2]);
    words.words[2]=TO_FIXED(context->parameters[3]);
    if(first>=0 && first<48) *native_fn_ov000_02210f08(first)=words;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
