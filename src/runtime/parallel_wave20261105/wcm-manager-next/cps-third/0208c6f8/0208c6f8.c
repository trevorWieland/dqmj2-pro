#include "context.h"
void native_main_0208c6f8(u8*buf) {
    CPS_SETUSHORT2(buf+6,2);
    native_fn_02008e0c(buf+8,buf+18,10);
    native_fn_02008e0c(native_data_021d01e0,buf+8,6);
    CPS_SETULONG2(buf+14,G.myip);
    native_fn_02008e0c(buf+18,buf-14,6);
    native_fn_02008e0c(native_data_021d01e0,buf-8,6);
    native_fn_0208bce8(buf-14,42,NULL,0);
}
