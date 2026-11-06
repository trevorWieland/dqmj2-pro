typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;

extern int native_selection_mask(int mask);
extern void native_selection_ids(u32 *ids, u8 *count);
extern u32 native_active_id(int index);

int saved_active_selection_remains(void) {
    s8 index;
    int permitted = 0;
    u32 ids[3];
    u8 count;
    if (!native_selection_mask(2))
        return 1;
    native_selection_ids(ids, &count);
    index = 0;
    do {
        int found = 0;
        u32 id = native_active_id(index);
        if (id) {
            s8 selected = 0;
            do {
                if (id == ids[selected]) {
                    found = 1;
                    break;
                }
                selected++;
            } while (selected < 3);
            if (!found) {
                permitted = 1;
                break;
            }
        }
        index++;
    } while (index < 3);
    return permitted;
}
