#include "context.h"
u32 native_ov001_021fb7ac(void) {
    if (native_data_ov001_02239a14[1] == 0) {
        native_fn_ov001_021fad98();
        ov001_begin_state_transition_021f1354(1, 2, 3, 1);
        ov001_select_mode_id_021f1438(native_fn_ov001_021f1414(0));
        native_fn_0205f210(1, 0);
        native_fn_02063d40();
        native_fn_0205e7a8(-1, 0x3A);
        native_fn_ov001_021fb75c();
        native_fn_ov001_021dc99c(*(u32 *)(native_data_ov001_02239a14 + 0x40));
        native_data_ov001_02239a14[1] = 10;
    } else if (native_data_ov001_02239a14[1] < 40) {
        native_data_ov001_02239a14[1]++;
    } else if (native_data_ov001_02239a14[1] == 40) {
        ov001_begin_state_transition_021f1354(1, 2, 5, 0);
        native_data_ov001_02239a14[1] = 50;
    } else if (native_data_ov001_02239a14[1] < 90) {
        native_data_ov001_02239a14[1]++;
    } else if (native_data_ov001_02239a14[1] == 90) {
        ov001_clear_state_flag4_021f14a4();
        native_data_ov001_02239a14[1] = 95;
    } else if (native_data_ov001_02239a14[1] == 95) {
        if (native_fn_ov001_021f14e4() == 0) {
            native_fn_ov001_021fb214(*(u32 *)(native_data_ov001_02239a14 + 0x40));
            native_data_ov001_02239a14[1] = 110;
        }
    } else if (native_data_ov001_02239a14[1] == 110) {
        native_data_ov001_02239a14[1] = 0;
        native_data_ov001_02239a14[0xA] = 15;
    }
    return 0;
}
