#include "context.h"
void native_main_0205a548(Context *context,const Instruction *instruction)
{
    int kind=(int)context->parameters[0];
    int index=(int)context->parameters[1];
    ObjectPrefix *object;
    if(kind==0)object=native_fn_02062a50(index);else object=native_fn_02062a88(index);
    context->parameters[0]=object?(float)native_fn_02067e54(object):0.0f;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
