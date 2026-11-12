#include "context.h"
void native_main_0204e850(Context *context,const Instruction *instruction)
{
    const Words3 *other=native_fn_ov000_021e5744((int)context->parameters[0]);
    const Words3 *base=ov000_saved_world_position_get_021e07b8(0);
    if(other) native_fn_ov000_021e0b88(native_fn_0202818c(base,other));
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
