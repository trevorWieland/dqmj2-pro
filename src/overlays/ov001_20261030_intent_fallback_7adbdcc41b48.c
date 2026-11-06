typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed int s32;
typedef struct {
    u16 action;
    u8 target_side;
    s8 target_slot;
    u8 marker;
    u8 unknown;
} ActionIntent;
extern ActionIntent native_data_ov001_02238d1c[3];
extern ActionIntent native_data_ov001_02238d2e[3];
void native_ov001_021e865c(s32 side, s32 slot) {
    if (side == 0) {
        native_data_ov001_02238d1c[slot].action = 6;
        native_data_ov001_02238d1c[slot].target_slot = -1;
        native_data_ov001_02238d1c[slot].marker = 1;
    } else {
        native_data_ov001_02238d2e[slot].action = 6;
        native_data_ov001_02238d2e[slot].target_slot = -1;
        native_data_ov001_02238d2e[slot].marker = 1;
    }
}
