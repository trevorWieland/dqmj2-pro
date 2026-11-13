typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct FeatureRecordView {
    u8 unobserved[0x440];
} FeatureRecordView;

typedef char FeatureRecordStride[(sizeof(FeatureRecordView) == 1088) ? 1 : -1];
extern void native_fn_02008e0c(const void *, void *, u32);
extern u32 native_fn_ov001_02210ba8(void *);
extern s32 ov001_count_candidates_02223f20(s32 *);
s32 native_ov001_02225854(s32 *, void *);
s32 native_ov001_022258d8(s32 *, void *);
