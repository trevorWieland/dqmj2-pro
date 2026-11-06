typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;

typedef struct {
    u8 prefix[0x33];
    u8 marker;
} MenuRecord;

typedef struct {
    u8 prefix[0x1FF];
    u8 first;
    u8 middle[0x11C];
    u8 second;
} MenuEntity;

extern int native_initial_menu_gate(void);
extern int native_menu_gate(int index);
extern void native_selected_ids(u32 *ids, int *count);
extern int native_record_mode(void);
extern MenuRecord *native_menu_record(u32 id);
extern MenuEntity *native_menu_entity(int group, u32 id);
extern void native_set_menu_enabled(int index, int enabled);

void saved_record33_menu_enable(void) {
    s8 index;
    int enabled = 1;
    u32 ids[3];
    int count;
    if (!native_initial_menu_gate()) {
        enabled = 0;
    } else if (!native_menu_gate(2)) {
        enabled = 0;
        native_selected_ids(ids, &count);
        index = 0;
        do {
            if (ids[index]) {
                if (native_record_mode() != 2) {
                    if (!native_menu_record(ids[index])->marker) {
                        enabled = 1;
                        break;
                    }
                } else {
                    MenuEntity *entity = native_menu_entity(0, ids[index]);
                    if (entity && (!entity->second || !entity->first)) {
                        enabled = 1;
                        break;
                    }
                }
            }
            index++;
        } while (index < 3);
    }
    native_set_menu_enabled(0, enabled);
}
