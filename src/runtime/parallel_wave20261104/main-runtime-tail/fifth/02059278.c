#include "context.h"
void native_main_02059278(Context *context, const Instruction *instruction)
{
    int bank = (int)context->parameters[0];
    int index = (int)context->parameters[1];
    int slot = (int)context->parameters[2];
    NativeRecord *record;
    if (bank == 0)
        record = native_fn_02062a50(index);
    else
        record = native_fn_02062a88(index);
    context->parameters[0] = (float)(record ? record->entries[slot].value : 0);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
