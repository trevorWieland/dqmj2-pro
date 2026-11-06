typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 prefix[46]; u8 flag0:1; u8 flag1:1; u8 other_flags:6; u8 remaining[41]; } NativeItemRecord;
typedef struct { u8 ids[12]; } RawSlotDefaults;
extern NativeItemRecord *native_item_table;
extern const RawSlotDefaults native_raw_slot_defaults;
extern u8 native_raw_slots[];
extern int saved_inventory_count_get(int);
extern int saved_raw_slot_set(int, int);
extern int saved_raw_option_set(int, int);
extern void saved_raw_marker_set(int);
extern u32 saved_secondary_set(int, int);
NativeItemRecord *saved_native_item_record(int id) { return &native_item_table[id]; }
int saved_inventory_nonzero_type_count(int category) {
    u8 index;
    int count;
    count = 0;
    index = 0;
    do {
        if (category == 0 && !saved_native_item_record(index)->flag0) goto next;
        if (category == 1 && !saved_native_item_record(index)->flag1) goto next;
        if (saved_inventory_count_get(index)) count++;
next:
        index++;
    } while (index < 255);
    return count;
}
void saved_raw_slots_initialize(void) {
    RawSlotDefaults initial = native_raw_slot_defaults;
    u8 index = 0;
    do {
        saved_raw_slot_set(index, initial.ids[index]);
        index++;
    } while (index < 12);
    index = 0;
    do {
        saved_raw_option_set(index, 127);
        index++;
    } while (index < 4);
    saved_raw_marker_set(127);
    saved_secondary_set(0, 1);
}
int saved_raw_slot_insert(int value) {
    int result = 0;
    u8 index = 0;
    u8 *slots = native_raw_slots;
    do {
        if (slots[index] == 127) {
            saved_raw_slot_set(index, value);
            result = 1;
            break;
        }
        index++;
    } while (index < 12);
    return result;
}
