typedef unsigned char u8;
typedef signed short s16;
typedef struct {
    s16 upper;
    s16 lower;
    s16 next;
    u8 at_lower;
    u8 at_upper;
} AllocationBounds;
typedef struct {
    u8 prefix[0xE0];
    s16 lower;
    s16 upper;
} AllocationTail;
extern int native_fn_020768d8(AllocationBounds *, int);
extern AllocationTail native_data_021c6434;
AllocationTail *native_main_020788bc(int rank) {
    AllocationBounds bounds;
    native_fn_020768d8(&bounds, rank);
    native_data_021c6434.lower = bounds.lower;
    native_data_021c6434.upper = bounds.upper;
    return &native_data_021c6434;
}
