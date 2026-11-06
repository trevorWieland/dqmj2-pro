typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct {
    u8 prefix[20];
    u32 id;
    u8 before_free[36];
    s16 free_points;
    u8 before_skills[60];
    u8 skills[10];
} SavedRecord;
typedef struct {
    u8 prefix[0xFC];
    int slot;
    u8 before_record[0xEC];
    SavedRecord *record;
    u8 before_target[0x60];
    int target;
} AllocationContext;
typedef struct {
    s16 upper;
    s16 lower;
    s16 next;
    u8 at_lower;
    u8 at_upper;
} AllocationBounds;
extern AllocationContext native_data_021c6234;
extern u8 *native_data_021c64d0[];
extern int native_fn_0207ad3c(const u8 *);
int native_main_020768d8(AllocationBounds *output, int rank) {
    int at_lower;
    u8 *table = native_data_021c64d0[native_data_021c6234.slot];
    SavedRecord *record = native_data_021c6234.record;
    u8 *slot = record->skills + native_data_021c6234.slot * 2;
    if (rank <= (u8)native_fn_0207ad3c(table)) {
        output->lower = rank > 0 ? *(table + rank - 1) : 0;
        output->next = rank < 10 ? table[rank] : *(table + rank - 1);
    } else {
        u8 *cursor = table + rank;
        output->lower = cursor[-2];
        output->next = cursor[-1];
    }
    output->upper = output->next;
    if (native_data_021c6234.target == output->lower) output->lower = rank > 1 ? *(table + rank - 2) : 0;
    if (output->lower < slot[1]) output->lower = slot[1];
    {
        int allocated = slot[1];
        int free_points = record->free_points;
        int available = allocated + free_points;
        if (output->upper > available) output->upper = available;
    }
    output->at_upper = output->upper == native_data_021c6234.target;
    at_lower = output->lower == native_data_021c6234.target;
    output->at_lower = at_lower;
    return at_lower;
}
