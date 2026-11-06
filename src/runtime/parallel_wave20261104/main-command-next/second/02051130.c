#include "context.h"
void native_main_02051130(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int third = (int)context->parameters[2];
    NativeVec3 a;
    int angle;
    NativeVec3 b;
    native_fn_ov000_021e77f8(third,&a);
    angle = native_fn_ov000_021e784c(third);
    b.x = 0;
    b.y = angle;
    b.z = 0;
    native_fn_ov000_02211188(first,&a,&b,second);
    native_fn_ov000_02212480(first,second,1);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
