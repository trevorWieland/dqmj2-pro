#include "context.h"
void native_main_02091864(ConnectionView *context)
{
    u8 temporary[48];
    native_fn_020917f8(temporary,native_data_020de87c,context);
    native_fn_020917f8(temporary+16,native_data_020de880,context);
    native_fn_020917f8(temporary+32,native_data_020de884,context);
    native_fn_02008e0c(temporary,context->master,48);
}
