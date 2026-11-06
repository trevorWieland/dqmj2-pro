#include "context.h"
void native_main_02050d4c(Context *context, const Instruction *instruction)
{
    int first = (int)context->parameters[0];
    int second = (int)context->parameters[1];
    int x = TO_FIXED(context->parameters[2]);
    int y = TO_FIXED(context->parameters[3]);
    int z = TO_FIXED(context->parameters[4]);
    int angle = TO_FIXED(context->parameters[5]);
    NativeVec3 a = {x,y,z};
    NativeVec3 b;
    b.x = 0;
    b.y = angle;
    b.z = 0;
    native_fn_ov000_02211188(first,&a,&b,second);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
