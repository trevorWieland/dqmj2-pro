#include "context.h"
void native_main_02058ab8(Context *context, const Instruction *instruction)
{
    ObjectRecord *record = native_fn_02062a50((int)context->parameters[0]);
    if (record) {
        u32 value = record->field31;
        if (value) {
            record->field31 = 0;
            native_fn_020630e4(value, -1, 0);
        }
        context->parameters[0] = (float)record->field31;
    } else
        context->parameters[0] = 0.0f;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
