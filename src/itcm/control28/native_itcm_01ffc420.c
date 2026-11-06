typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_01ffb340(void);
extern u32 native_fn_020babd8(u32);
extern u32 native_fn_020bb144(u32);
typedef struct { u8 cursor; u8 probe; u8 count; } ScanState;
extern ScanState native_data_021d4100;
extern u8 native_data_021d41f4[];
extern u8 native_data_021d41fc[];
void native_itcm_01ffc420(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u8 temp_r2;
    u8 temp_r2_2;
    s8 temp_r4;

    temp_r4 = (s8) native_data_021d41f4[native_data_021d4100.cursor];
    if (temp_r4 != -1) {
        temp_r0 = native_fn_020babd8((u32) temp_r4);
        switch (temp_r0) {
        case 1:
            if (native_data_021d41fc[temp_r4] != 1) {
                M2C_FIELD((void *) native_fn_01ffb340(), s8 *, 0x11) = 1;
            }
            native_data_021d41fc[(s8) native_data_021d41f4[native_data_021d4100.cursor]] = 1;
            break;
        case 4:
            if (native_data_021d41fc[temp_r4] != 2) {
                M2C_FIELD((void *) native_fn_01ffb340(), s8 *, 0x11) = 1;
            }
            native_data_021d41fc[(s8) native_data_021d41f4[native_data_021d4100.cursor]] = 2;
            break;
        default:
            if (native_data_021d41fc[temp_r4] != 3) {
                M2C_FIELD((void *) native_fn_01ffb340(), s8 *, 0x11) = 1;
            }
            native_data_021d41fc[(s8) native_data_021d41f4[native_data_021d4100.cursor]] = 3;
            break;
        }
    }
    ++native_data_021d4100.cursor;
    if (native_data_021d4100.cursor == 8) {
        native_data_021d4100.cursor = 0;
    }
    if (native_data_021d41fc[native_data_021d4100.probe] == 0) {
        native_fn_020bb144((u32) native_data_021d4100.probe);
        if (native_fn_020bb144((u32) native_data_021d4100.probe) == 4) {
            temp_r0_2 = native_fn_020babd8((u32) native_data_021d4100.probe);
            if ((temp_r0_2 != 1) && (temp_r0_2 != 4)) {

            } else {
                native_data_021d41f4[native_data_021d4100.count] = native_data_021d4100.probe;
                native_data_021d41fc[native_data_021d4100.probe] = 1;
                native_data_021d4100.count = (u8) (native_data_021d4100.count + 1);
                M2C_FIELD((void *) native_fn_01ffb340(), s8 *, 0x11) = 1;
            }
        }
    }
    ++native_data_021d4100.probe;
    if ((u32) native_data_021d4100.probe >= 0x40U) {
        native_data_021d4100.probe = 0U;
    }
}
