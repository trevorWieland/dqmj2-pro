typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ChildScorePrefix {
    u8 unknown0[0x28];
    s16 value28;
    u8 unknown2a[6];
    s16 value30;
    u8 unknown32[0xb1 - 0x32];
    u8 flagb1;
    u8 unknownb2[0xcc - 0xb2];
    u8 valuecc;
} ChildScorePrefix;
typedef struct ChildScoreRecord {
    u8 unknown0[0x1e8];
    const ChildScorePrefix *child;
    u8 unknown1ec[0x440 - 0x1ec];
} ChildScoreRecord;
typedef char ChildScoreRecordStride[(sizeof(ChildScoreRecord) == 0x440) ? 1 : -1];
extern void native_fn_02008e0c(const void *, void *, u32);
extern s32 ov001_count_candidates_02223f20(s32 *);
s32 native_ov001_02226290(s32 *, const void *);
s32 native_ov001_02226310(s32 *, const void *);
s32 native_ov001_022263d8(s32 *, const void *);
