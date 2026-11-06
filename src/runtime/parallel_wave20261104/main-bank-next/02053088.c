#include "context.h"
void native_main_02053088(Context *context, const Instruction *instruction)
{
    int count = 0;
    int wanted = (int)context->parameters[0];
    NativeRecord *record = native_fn_02062b00();
    int index = 0;
    do {
        if (record->field14 && wanted == record->field18)
            ++count;
        ++index;
        ++record;
    } while (index < 100);
    context->parameters[0] = (float)count;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
