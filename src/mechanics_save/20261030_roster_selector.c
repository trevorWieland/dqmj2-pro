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
    s8 group;
    u8 reserved;
    u8 x;
    u8 y;
} RosterSelection;
__declspec(align(4)) extern RosterRow native_data_021c4a04[];
__declspec(align(4)) extern RosterSelection native_data_021c4968;
extern u32 native_fn_0206d250(s32 sprite);
s32 native_main_0206ba88(void) {
    RosterRow *rows = native_data_021c4a04;
    s8 index = 0;
    RosterSelection *selection = &native_data_021c4968;
    do {
        if (rows[index].enabled != 0 && selection->group == rows[index].group &&
            selection->x == rows[index].x && rows[index].y <= selection->y) {
            s32 metric = (s32) native_fn_0206d250(rows[index].sprite);
            s32 end = rows[index].y;
            end += metric;
            if (end >= selection->y) {
                return index;
            }
        }
        index++;
    } while (index < 15);
    return -1;
}
