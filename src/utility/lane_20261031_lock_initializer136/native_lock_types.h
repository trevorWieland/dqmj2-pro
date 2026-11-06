typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct RawLockWord {
    u32 value;
    u16 owner;
    u16 extension;
} RawLockWord;
typedef char NativeU32IsFourBytes[(sizeof(u32)==4)?1:-1];
typedef char NativeLockMinimumViewIsEightBytes[(sizeof(RawLockWord)==8)?1:-1];
