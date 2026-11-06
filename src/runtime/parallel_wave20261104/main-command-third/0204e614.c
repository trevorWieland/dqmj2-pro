#include "context.h"
void native_main_0204e614(Context *context,const Instruction *instruction)
{
    int first=TO_FIXED(context->parameters[0]);
    int second=TO_FIXED(context->parameters[1]);
    int third=TO_FIXED(context->parameters[2]);
    OpaqueFields *destination;
    OpaqueFields *other;
    native_fn_ov000_021e0b60(first,second,third);
    destination=native_fn_ov000_021e07ac();
    other=native_fn_ov000_021e07ac();
    destination->field110=other->field70;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
