#include "context.h"
u32 native_ov006_021f7c64(void) {
    u32 var_r0_2;
    u32 var_r0;

    var_r0 = native_fn_ov006_02203188(0);
    if ((var_r0 == 0) && ((*native_data_ov006_0221c0cc != 0) || (var_r0 = native_fn_ov006_02203188(1), (var_r0 == 0)))) {
        var_r0 = native_fn_ov006_021f23c4();
        if (var_r0 != 0) {
            if (*native_data_ov006_0221c0cc != 0) {
                var_r0_2 = 1;
            } else {
                var_r0_2 = 0;
            }
            native_fn_ov006_021f4eb8(var_r0_2);
            native_fn_ov006_021f221c();
            native_fn_ov006_02203690(0);
            if (*native_data_ov006_0221c0cc == 0) {
                native_fn_ov006_021f2774();
                native_fn_ov006_02203954(1, 1);
            }
            native_fn_ov006_02203954(0, 0x15);
            if (*native_data_ov006_0221c0cc == 0) {
                native_fn_ov006_021f52d8(2, 1);
                return native_fn_ov006_021f52cc(native_fn_ov006_021fd11c);
            }
            native_fn_ov006_021f52d8(0, 0);
            var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021f7da4);
            
            return var_r0;
        }
    }
    return var_r0;
}
