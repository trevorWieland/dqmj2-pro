#include "context.h"

/* Open a task through the shared task builder. A request byte of 0xff reuses
   the stored task id instead of storing a new one. Returns whether the task
   builder produced a live handle. */
s32 native_ov000_021d900c(u8 request)
{
    u8 record[16];
    s8 word_1;
    u8 word_2;
    u8 word_3;
    s32 handle;

    if (request == 0xff)
        request = native_data_ov000_0223142c.field_7c0;
    else
        native_data_ov000_0223142c.field_7c0 = request;
    native_fn_ov000_021df220(request, &word_1, &word_2, &word_3);
    native_fn_0201d444(record, &native_data_ov000_0222e19c, word_1, word_2, (s32)word_3);
    handle = native_fn_0203cc2c(record, -1);
    native_data_ov000_022303e8 = handle;
    return handle != 0;
}
