#include "context.h"
void native_main_0205a3b8(Context *context,const Instruction *instruction)
{
    int kind=(int)context->parameters[0];
    int index=(int)context->parameters[1];
    u8 wanted=(u32)context->parameters[2];
    u8 expected=(u32)context->parameters[3];
    u8 temporary[64];
    u8 output[32];
    ObjectPrefix *object;
    if(kind==0) {
        object=native_fn_02062a50(index);
        if(object) {
            native_fn_0207b460(object->field18,object->field1a,object->field7a,temporary);
            native_fn_0207c078(object->field18,object->field1a,temporary,output);
            if(output[wanted]==expected) { context->parameters[0]=1.0f;END_COMMAND(0); }
        }
    }
    else {
        object=native_fn_02062a88(index);
        if(object) {
            native_fn_0207b460(object->field18,object->field1a,object->field7a,temporary);
            native_fn_0207c078(object->field18,object->field1a,temporary,output);
            if(output[wanted]==expected) { context->parameters[0]=1.0f;END_COMMAND(0); }
        }
    }
    context->parameters[0]=0.0f;
    END_COMMAND(0);
}
