#include "context.h"
void native_main_0205a094(Context *context,const Instruction *instruction)
{
    int kind=(int)context->parameters[0];
    int index=(int)context->parameters[1];
    ObjectPrefix *object;
    if(kind==0)object=native_fn_02062a50(index);else object=native_fn_02062a88(index);
    context->parameters[0]=object?(float)native_fn_02044dc4(object->field18,object->field1a):0.0f;
    context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=0;
}
