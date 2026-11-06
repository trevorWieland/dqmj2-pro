#include "context.h"
void native_main_02052e38(Context *context, const Instruction *instruction)
{
    int value = 3;
    int index = 0;
    do {
        CountRecord *record = native_fn_02062a50(index);
        if (record) value -= native_fn_02044cdc(record->slot18) + 1;
        index++;
    } while (index < 3);
    if (100 - native_fn_020629e0() < value) {
        value = 100 - native_fn_020629e0();
    }
    if (value < 0) value = 0;
    context->parameters[0] = (float)value;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
