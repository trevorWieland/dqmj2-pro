#include "context.h"
void native_main_02052f78(Context *context, const Instruction *instruction)
{
    int result = 0;
    int index;
    int value = (int)context->parameters[0];
    index = 0;
    do {
        CountRecord *record = native_fn_02062a50(index);
        if (record && record->slot18 == value) result++;
        index++;
    } while (index < 3);
    context->parameters[0] = (float)result;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
