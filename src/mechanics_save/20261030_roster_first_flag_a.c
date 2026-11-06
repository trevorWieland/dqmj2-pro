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
__declspec(align(4)) extern RosterRow native_data_021c4a04[];
u32 native_main_0206bdc8(void) {
    RosterRow *rows = native_data_021c4a04;
    u8 index = 0;
    do {
        if (rows[index].enabled != 0 && rows[index].flag_a != 0) {
            return rows[index].uid;
        }
        index++;
    } while (index < 15);
    return 0;
}
