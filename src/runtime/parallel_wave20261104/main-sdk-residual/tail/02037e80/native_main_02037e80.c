#include "context_00.h"
BOOL native_main_02037e80 (void)
{
    if (!native_data_main_020f1f64.field_0004) {
        while (native_fn_020095e8(0 ) != 0) {
        }
        if (!native_fn_02009a0c(native_data_main_020f1f64.field_0008)) {
            return 0 ;
        }
        if (native_data_main_020f1f64.field_0000 < 0) native_data_main_020f1f64.field_0000 = 1;
        native_fn_02009400(&native_data_main_020f1fa0[ native_data_main_020f1f64.field_0000 ]);
        native_data_main_020f1f64.field_0008 = native_fn_020099e0();
        if (native_data_main_020f1f64.field_0000 == 0) native_data_main_020f1f64.field_0000 = 1;
        else native_data_main_020f1f64.field_0000 = 0;
        native_fn_020072d0(&native_data_main_020f1fa0[ native_data_main_020f1f64.field_0000 ], sizeof(SNDDriverInfo));
        (void)native_fn_020097b8(0 );
        return 1 ;
    } else {
        native_fn_02009400(&native_data_main_020f1fa0[0]);
        native_data_main_020f1f64.field_0008 = native_fn_020099e0();
        native_data_main_020f1f64.field_0004 = 0 ;
        return 0 ;
    }
}
