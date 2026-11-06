#include "context.h"
void native_main_0205930c(Context *context, const Instruction *instruction)
{
    int bank = (int)context->parameters[0];
    int index = (int)context->parameters[1];
    NativeRecord *record;
    if (bank == 0)
        record = native_fn_02062a50(index);
    else
        record = native_fn_02062a88(index);
    context->parameters[0] = (float)(record ? record->field1e : 0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
