#include "context.h"
void native_main_0204e740(Context *context,const Instruction *instruction)
{
    const Words3 *words=native_fn_ov000_021e07b8(0);
    context->parameters[0]=(float)words->words[0]/4096.0f;
    context->parameters[1]=(float)words->words[1]/4096.0f;
    context->parameters[2]=(float)words->words[2]/4096.0f;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
