#include "context.h"
void native_main_02051510(Context *context,const Instruction *instruction)
{
    short first = (int)context->parameters[0];
    short second = (int)context->parameters[1];
    MatrixRecord *record = (MatrixRecord *)native_fn_ov000_0221220c(first,second);
    Matrix33 d,c,b,a;
    record->slot88[0] = native_fn_02028158(TO_FIXED(context->parameters[2]));
    record->state09 = 1;
    record->slot88[1] = native_fn_02028158(TO_FIXED(context->parameters[3]));
    record->state09 = 1;
    record->slot88[2] = native_fn_02028158(TO_FIXED(context->parameters[4]));
    record->state09 = 1;
    if (record->state09) {
        native_fn_02000ce8(&a);
        native_fn_020280a0(&b,record->slot88[2]);
        native_fn_02028044(&c,record->slot88[1]);
        native_fn_02027fe8(&d,record->slot88[0]);
        native_fn_02000e1c(&c,&b,&a);
        native_fn_02000e1c(&d,&a,&record->matrix94);
        record->state09 = 0;
    }
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
