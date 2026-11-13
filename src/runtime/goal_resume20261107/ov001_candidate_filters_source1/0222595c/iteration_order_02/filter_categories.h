typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct CandidateChildPrefix {
    u8 unknown0[0x2a];
    s16 species;
} CandidateChildPrefix;
typedef struct CandidateRosterRecord {
    u8 unknown0[0x1e8];
    const CandidateChildPrefix *child;
    u8 unknown1ec[0x440 - 0x1ec];
} CandidateRosterRecord;
typedef struct SpeciesPrefix {
    u8 unknown0[4];
    u16 unknown4:4;
    u16 category:4;
    u16 unknown8:8;
} SpeciesPrefix;
typedef char CandidateRosterStride[(sizeof(CandidateRosterRecord) == 0x440) ? 1 : -1];
extern void native_fn_02008e0c(const void *, void *, u32);
extern u32 native_fn_020449d4(s32);
extern int native_fn_0207b02c(int, int);
extern s32 ov001_count_candidates_02223f20(s32 *);
s32 native_ov001_0222595c(s32 *, const void *, s32);
