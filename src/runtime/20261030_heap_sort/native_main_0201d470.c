typedef signed char s8;
typedef signed int s32;
typedef unsigned int u32;
void native_main_0201d470(s8 *array, u32 count, u32 width, s32 (*compare)(void *, void *)) {
    s8 *root_record;
    s8 *last_record;
    u32 root_bytes;
    u32 negative_width;
    s8 parent_byte;
    s8 root_byte;
    u32 root_index;
    u32 heap_count;
    u32 child_index;
    s8 *child_record;
    s8 *parent_record;
    u32 swap_remaining;
    s8 *swap_left;
    s8 *swap_right;
    u32 remaining;
    s8 *child_cursor;
    heap_count = count;
    if (heap_count < 2U) {
        return;
    }
    root_index = (heap_count >> 1) + 1;
    root_record = array + width * (root_index - 1);
    last_record = array + width * (heap_count - 1);
    root_bytes = root_index * width;
    negative_width = width * -1;
root_loop:
    if (root_index > 1U) {
        root_index -= 1;
        root_bytes -= width;
        root_record -= width;
    } else {
        swap_remaining = width;
        swap_right = last_record;
        swap_left = root_record;
        if (width != 0) {
            do {
                root_byte = *swap_left;
                swap_remaining -= 1;
                *swap_left = (s8) *swap_right;
                swap_left += 1;
                *swap_right = root_byte;
                swap_right += 1;
            } while (swap_remaining != 0);
        }
        heap_count -= 1;
        if (heap_count == 1) {
            return;
        }
        last_record -= width;
    }
    child_index = root_index;
    child_record = array + (root_bytes + negative_width);
    if (heap_count >= (u32) (root_index * 2)) {
        do {
    child_index *= 2;
    parent_record = child_record;
    child_record = (s8 *) ((width * (child_index - 1)) + (s32) array);
    if ((heap_count > child_index) && (compare(child_record, child_record + width) < 0)) {
        child_index += 1;
        child_record += width;
    }
    if (compare(parent_record, child_record) >= 0) {
        goto root_loop;
    }
    remaining = width;
    child_cursor = child_record;
    if (width != 0) {
        do {
            parent_byte = *parent_record;
            *parent_record = *child_cursor;
            remaining -= 1;
            parent_record += 1;
            *child_cursor = parent_byte;
            child_cursor += 1;
        } while (remaining != 0);
    }
        } while (heap_count >= (u32) (child_index * 2));
    }
    goto root_loop;
}
