#include "context.h"
void native_main_02053468(Context *context, const Instruction *instruction)
{
    int result = -1;
    int index = (int)context->parameters[0];
    if (native_fn_02062a78(index)) {
        NativeRecord *record = native_fn_02062a88(index);
        result = native_fn_02044cdc(record->field18);
    }
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
