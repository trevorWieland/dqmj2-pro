#include "context.h"
void native_main_0205392c(Context *context, const Instruction *instruction)
{
    int result = -1;
    int index = (int)context->parameters[0];
    if (native_fn_02062a68(index)) {
        NativeRecord *record = native_fn_02062a50(index);
        result = native_fn_020535b4(record);
    }
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
