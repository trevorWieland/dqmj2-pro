#include "context.h"
void native_ov001_0222cd84(s32 index) {
    s32 offset = index * 132;
    native_fn_02044ff4(native_data_ov001_022498fc + offset,native_data_ov001_02249830[index],0);
    *(u16*)(native_data_ov001_02249914 + offset) = (u16)native_data_ov001_02249830[index];
    switch (native_fn_020449d4(native_data_ov001_02249830[index])->kind) {
    case 1:
    case 2:
    case 3:
        switch (native_data_ov001_02249828[0]) {
        case 50:
            native_data_ov001_02249916[offset] = 1;
            break;
        case 100:
        case 101:
            native_data_ov001_02249916[offset] = (u8)(native_fn_0203d294(2) + 1);
            break;
        default:
            break;
        }
        break;
    case 4:
    case 5:
    case 6:
        switch (native_data_ov001_02249828[0]) {
        case 50:
            native_data_ov001_02249916[offset] = 0;
            break;
        case 100:
        case 101:
            native_data_ov001_02249916[offset] = (u8)native_fn_0203d294(2);
            break;
        default:
            break;
        }
        break;
    default:
        native_data_ov001_02249916[offset] = 0;
        break;
    }
    native_data_ov001_02249917[offset] = (u8)native_fn_0203d294(3);
}
