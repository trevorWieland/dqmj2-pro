#include "action_types_20261030.h"
extern u32 native_fn_02072ed4(u32 index);
extern u8 native_data_021c5a16[];
extern u8 native_data_021c5a19[];
u32 native_main_02072b00(Selection *selection) {
    if (native_data_021c5a16[selection->x * 9] != 0 && native_fn_02072ed4(selection->x) != 0) {
        native_data_021c5a19[selection->x * 9] = 1;
        return (s8)(selection->x + 1);
    }
    native_data_021c5a19[selection->x * 9] = 0;
    return 0;
}
