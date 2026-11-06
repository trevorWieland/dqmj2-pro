typedef unsigned char u8;
typedef unsigned int u32;
extern u32 native_item_bits[];
extern u8 native_main[];
extern u8 native_item_queues[];
extern u8 native_item_buffer[];
extern u8 *native_item_record(int);
extern int native_item_queue_compact(int);
extern int saved_item_recent_find(int);
extern void native_fill(void *, int, u32);
extern void native_copy(const void *, void *, u32);
int saved_item_observed_get(int item) {
    return (native_item_bits[item >> 5] & (1 << (item & 31))) != 0;
}
u8 saved_item_recent_insert(int item) {
    u8 family = native_item_record(item)[44] == 7;
    u8 saved[10];
    u8 index;
    u8 count;
    if (!item) return 0;
    index = 0;
    do {
        saved[index] = native_main[0x3748 + family * 12 + index];
        native_main[0x3748 + family * 12 + index] = 0;
        index++;
    } while (index < 10);
    native_item_queues[family * 12] = item;
    count = 1;
    for (index = 0; index < 9; index++) {
        if (saved[index]) {
            native_main[0x3748 + family * 12 + count] = saved[index];
            count = count + 1;
        }
    }
    return native_item_queue_compact(family);
}
int saved_item_observed_set(int item) {
    int previous = saved_item_observed_get(item);
    if (!saved_item_observed_get(item)) {
        saved_item_recent_insert(item);
        native_item_bits[item >> 5] |= 1 << (item & 31);
    }
    return previous;
}
int saved_item_recent_remove(int item) {
    u8 family;
    int index;
    if (!item) return 0;
    family = native_item_record(item)[44] == 7;
    index = saved_item_recent_find(item);
    if (index == -1) return 0;
    (native_item_queues + family * 12)[index] = 0;
    return native_item_queue_compact(family);
}
void saved_item_buffer_set(const void *data) {
    native_fill(native_item_buffer, 0, 20);
    native_copy(data, native_item_buffer, 20);
}
u8 *saved_item_buffer_get(void) { return native_item_buffer; }
