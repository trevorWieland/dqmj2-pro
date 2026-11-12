#include "context.h"
void native_main_0204eac8(Context *context,const Instruction *instruction)
{
    const Words3 *base=ov000_saved_world_position_get_021e07b8(0);
    Words3 words;
    int fourth;
    words.words[0]=base->words[0];
    words.words[1]=TO_FIXED(context->parameters[0]);
    words.words[2]=base->words[2];
    fourth=TO_FIXED(context->parameters[1]);
    native_fn_ov000_021e2ce8(&words,fourth);
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
