typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u32 uid;
    u16 reserved;
    u8 x;
    u8 y;
    u8 group;
    u8 enabled;
    u8 flag_a;
    u8 flag_b;
    s8 sprite;
    u8 padding;
    u8 tag_a;
    u8 tag_b;
} RosterRow;
typedef struct {
    u8 prefix[6];
    u8 flag6;
    u8 reserved[13];
    u32 previous_uid;
    u32 candidate_uid;
} RosterCurrent;
typedef struct {
    s8 group;
    u8 prefix[3];
    u8 flag4;
    u8 reserved;
    u8 flag6;
} RosterChoice;
__declspec(align(4)) extern RosterRow native_data_021c4a04[];
__declspec(align(4)) extern RosterCurrent native_data_021c48f8;
__declspec(align(4)) extern RosterChoice native_data_021c4968;
extern u32 native_fn_0206c0b0(void);
extern u32 native_fn_0206c0d0(void);
extern u32 native_fn_0206c0e0(void);
extern u32 native_fn_020c0a7c(void);
extern u32 native_fn_02069000(void);
extern u32 native_fn_020bf858(RosterChoice *choice);
extern u32 native_fn_0206bb1c(void);
extern u32 native_fn_0206bdc8(void);
u32 native_main_0206be2c(void) {
    if (native_fn_0206c0b0() != 0) {
        if (native_fn_0206c0e0() == 0) {
            native_data_021c48f8.candidate_uid = native_data_021c4a04[(s32) native_fn_0206c0d0()].uid;
        } else {
            native_data_021c48f8.candidate_uid = native_fn_020c0a7c();
        }
    } else if (native_data_021c4968.flag6 != 0) {
        native_data_021c48f8.candidate_uid = 0;
    } else if (native_data_021c48f8.flag6 != 0 && (u32) native_data_021c4968.group == native_fn_02069000()) {
        native_data_021c48f8.candidate_uid = native_fn_020bf858(&native_data_021c4968);
    } else if (native_fn_0206bb1c() != 0) {
        native_data_021c48f8.candidate_uid = native_fn_0206bb1c();
    } else if (native_data_021c4968.flag4 != 0) {
        native_data_021c48f8.candidate_uid = native_fn_0206bdc8();
    } else {
        native_data_021c48f8.candidate_uid = 0;
    }
    {
        u32 candidate = native_data_021c48f8.candidate_uid;
        if (candidate != native_data_021c48f8.previous_uid) {
            native_data_021c48f8.previous_uid = candidate;
            return candidate;
        }
    }
    return 0;
}
