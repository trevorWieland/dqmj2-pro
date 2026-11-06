#include "context.h"
void native_main_02052c8c(Context *context, const Instruction *instruction)
{
    int index;
    int count = native_fn_02062ad0();
    u8 temporary[64];
    index = 0;
    context->parameters[0] = -1.0f;
    context->parameters[1] = -1.0f;
    context->parameters[2] = -1.0f;
    if (count > 0) {
        do {
            MeasureRecord *record = native_fn_02062a88(index);
            float denominator;
            float numerator;
            float ratio;
            native_fn_0207b460(record->field18,record->field1a,record->data7a,temporary);
            denominator = (float)native_fn_0207c3d8(record->data20,temporary);
            numerator = (float)native_fn_0207c1b8(record->data20,temporary);
            ratio = numerator / denominator;
            if (ratio <= 0.2f) context->parameters[index] = 1.0f;
            else if (ratio < 1.0f) context->parameters[index] = 3.0f;
            else if (ratio == 1.0f) context->parameters[index] = 2.0f;
            else context->parameters[index] = 0.0f;
            index++;
        } while (index < count);
    }
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
