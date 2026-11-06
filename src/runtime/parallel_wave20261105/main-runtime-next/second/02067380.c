#include "context.h"
u32 native_main_02067380(void)
{
    u32 result = 0;
    if (native_data_021c36fc.step4 == 65535) return 1;
    switch (native_data_020de23c.current4) {
    case 0:
        result = 1;
        break;
    case 2:
        if (native_data_021c36fc.step4 == 0) {
            native_fn_02041510(1, 2, 10);
            native_fn_02041560(10);
            native_fn_020414b0(0x21);
            native_data_021c36fc.step4 = 10;
        } else if (native_data_021c36fc.step4 == 10) {
            if (native_data_021c36fc.choice0 == 3) native_data_021c36fc.step4 = 20;
            else if (native_data_021c36fc.choice0 == 1) {
                native_fn_02041510(0, 2, 10);
                native_fn_020418e8(10, 10);
                native_fn_020414b0(0x3f);
                native_data_021c36fc.step4 = 20;
            } else if (native_data_021c36fc.choice0 == 2) {
                native_fn_02041510(1, 2, 10);
                native_fn_020418e8(10, 10);
                native_fn_020414b0(0x3f);
                native_data_021c36fc.step4 = 20;
            } else if (native_data_020de23c.current4 != native_data_020de23c.desired0) {
                native_fn_02041510(1, 2, 10);
                native_fn_020418e8(10, 10);
                native_fn_020414b0(0x3f);
                native_data_020de23c.current4 = native_data_020de23c.desired0;
                native_data_021c36fc.step4 = 65535;
            }
        } else if (native_data_021c36fc.step4 == 20) {
            if (native_fn_02041800() != 1) result = 1;
        }
        break;
    case 1:
    case 3:
        if (native_data_021c36fc.step4 == 0) {
            native_fn_ov000_02214120();
            if (!native_fn_020407cc()) native_fn_02041510(1, 2, 10);
            else native_fn_020407bc(0);
            native_data_021c36fc.step4 = 5;
        } else if (native_data_021c36fc.step4 == 5) {
            if (native_fn_02041800() != 1) native_data_021c36fc.step4 = 10;
        } else if (native_data_021c36fc.step4 == 10) {
            if (native_fn_ov000_022149dc()) {
                native_data_020de23c.current4 = native_data_020de23c.desired0;
                native_data_021c36fc.step4 = 65535;
                result = 1;
            }
        }
        break;
    }
    return result;
}
