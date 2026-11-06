typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct State {
    u8 prefix[0x44];
    u32 mask;
    s32 count;
    u8 slots[32];
    u8 gap[0xB4];
    u32 references;
} State;
