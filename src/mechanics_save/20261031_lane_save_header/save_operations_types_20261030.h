typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct SaveOperationState {
    u8 prefix[0x12];
    s16 first;
    u8 gap[2];
    s16 second;
    u32 headerValid;
} SaveOperationState;
typedef struct SaveHeaderSummary {
    u8 prefix[0x5d];
    u8 rawCount;
} SaveHeaderSummary;
extern SaveOperationState native_data_021c6544;
extern SaveHeaderSummary native_data_021c65d0;
extern u8 native_data_021c65a8[];
extern int native_fn_0207df2c(u32 index, void *output);
