#include "context.h"
void native_main_02053198(Context *context, const Instruction *instruction)
{
    int result = -1;
    int index = (int)context->parameters[0];
    if (native_fn_02062a78(index)) {
        NativeRecord *record = native_fn_02062a88(index);
        result = native_fn_02044dc4(record->field18, record->field1a);
    }
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
