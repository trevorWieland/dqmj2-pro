#include "context.h"
void native_main_0204de70(ExtendedContext *context,const Instruction *instruction)
{
    Words3 words;
    words.words[0]=TO_FIXED(context->parameters[0]);
    words.words[1]=TO_FIXED(context->parameters[1]);
    words.words[2]=TO_FIXED(context->parameters[2]);
    native_fn_ov000_021e07ac()->field178=words;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
