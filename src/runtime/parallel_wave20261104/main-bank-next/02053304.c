#include "context.h"
void native_main_02053304(Context *context, const Instruction *instruction)
{
    int result = -1;
    int index = (int)context->parameters[0];
    if (native_fn_02062a68(index)) {
        NativeRecord *record = native_fn_02062a50(index);
        result = record->field1e;
    }
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
