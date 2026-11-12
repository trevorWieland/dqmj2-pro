typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct CompatibilityRecordView {
    u8 unobserved000[0x234];
    s8 stage;
    u8 unobserved235[0x31f - 0x235];
    u8 category;
    u8 unobserved320[0x440 - 0x320];
} CompatibilityRecordView;

typedef char CompatibilityRecordStride[(sizeof(CompatibilityRecordView) == 0x440) ? 1 : -1];
extern void native_fn_02008e0c(const void *, void *, u32);
extern s32 ov001_count_candidates_02223f20(s32 *);
s32 native_ov001_02226598(s32 *, const void *, const void *);
