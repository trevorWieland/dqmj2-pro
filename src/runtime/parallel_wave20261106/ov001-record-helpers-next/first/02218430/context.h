typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ChildView { u8 unknown0[8]; u8 values8[6]; } ChildView;
typedef struct Object440 {
    u8 unknown0[0x1e8];
    ChildView *child1e8;
    u8 unknown1ec[0x322 - 0x1ec];
    u8 field322;
    u8 field323;
    u8 unknown324[0x35e - 0x324];
    u8 values35e[0x440 - 0x35e];
} Object440;
extern u32 native_fn_0207b004(s32, u32);
s32 native_ov001_02218430(Object440 *, s32 *, u32);
