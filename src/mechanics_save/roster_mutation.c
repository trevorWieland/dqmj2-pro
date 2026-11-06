typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u8 prefix[20]; u32 id; s16 species; u8 variant; u8 tail[105]; } SavedRecord;
typedef struct { u8 prefix[28]; u32 party[3]; u32 reserve[3]; } SavedGroups;
extern SavedRecord native_records[100];
extern SavedGroups native_groups;
extern SavedRecord *saved_record_by_id(u32);
extern int native_record_exists(u32);
extern u32 native_record_next_id(void);
extern int native_obtained_set(int, int);
extern int native_seen_set(int, int);
extern int native_category(int);
extern int native_event16_get(void);
extern void native_record_features_observe(SavedRecord *);
extern int native_records_sort(void);
extern void native_fill(void *, u32, u32);
extern void native_secondary_set(int, int);
extern void native_feature_collect(int, int, const u8 *, u8 *);
extern void native_feature_observed_set(int);
extern SavedRecord *native_record_base(void);
extern int native_record_skill_count(u32);
extern u8 *native_record_skill_pointer(u32, int);
extern void native_skill_observe(int, int, int);
int saved_party_has_id(u32 id) {
    int index;
    int result = 0;
    if (id) {
        SavedGroups *groups = &native_groups;
        index = 0;
        do {
            if (((SavedGroups *)((u8 *)groups + index * 4))->party[0] == id) { result = 1; break; }
            index++;
        } while (index < 3);
    }
    return result;
}
int saved_reserve_has_id(u32 id) {
    int index;
    int result = 0;
    if (id) {
        SavedGroups *groups = &native_groups;
        index = 0;
        do {
            if (((SavedGroups *)((u8 *)groups + index * 4))->reserve[0] == id) { result = 1; break; }
            index++;
        } while (index < 3);
    }
    return result;
}
SavedRecord *saved_record_first_free(void) {
    SavedRecord *result = 0;
    int index = 0;
    SavedRecord *record = native_records;
    do {
        if (!record->id) { result = record; break; }
        index++;
        record++;
    } while (index < 100);
    return result;
}
u32 saved_record_create(int species, int variant) {
    u32 result = 0;
    SavedRecord *record = saved_record_first_free();
    if (record) {
        native_fill(record, 0, 132);
        record->species = species;
        record->variant = variant;
        record->id = native_record_next_id();
        result = record->id;
        native_obtained_set(species, variant);
        native_seen_set(species, variant);
        if (native_category(record->species) != 2 || native_event16_get()) native_record_features_observe(record);
        native_records_sort();
    }
    return result;
}
int saved_party_insert_id(u32 id) {
    int result = 0;
    int index;
    if (native_record_exists(id)) {
        SavedGroups *groups = &native_groups;
        if (!saved_party_has_id(id)) {
        index = 0;
        do {
            if (!((SavedGroups *)((u8 *)groups + index * 4))->party[0]) { ((SavedGroups *)((u8 *)groups + index * 4))->party[0] = id; result = 1; break; }
            index++;
        } while (index < 3);
    }
    }
    return result;
}
u32 saved_party_remove_index(u32 index) {
    u32 result = 0;
    SavedGroups *groups = &native_groups;
    if (index < 3) {
        result = ((SavedGroups *)((u8 *)groups + index * 4))->party[0];
        if (result) {
            if ((int)index < 2) do {
                ((SavedGroups *)((u8 *)groups + index * 4))->party[0] = ((SavedGroups *)((u8 *)groups + index * 4))->party[1];
                index++;
            } while ((int)index < 2);
            groups->party[2] = 0;
        }
    }
    return result;
}
int saved_reserve_insert_id(u32 id) {
    int result = 0;
    int index;
    if (native_record_exists(id)) {
        SavedGroups *groups = &native_groups;
        if (!saved_reserve_has_id(id)) {
        index = 0;
        do {
            if (!((SavedGroups *)((u8 *)groups + index * 4))->reserve[0]) {
                ((SavedGroups *)((u8 *)groups + index * 4))->reserve[0] = id;
                result = 1;
                native_secondary_set(14, 1);
                native_secondary_set(15, 1);
                break;
            }
            index++;
        } while (index < 3);
    }
    }
    return result;
}
u32 saved_reserve_remove_index(int index) {
    SavedGroups *groups = &native_groups;
    u32 result = 0;
    if (index >= 0 && index < 3) {
        u32 current = ((SavedGroups *)((u8 *)groups + index * 4))->reserve[0];
        if (current) {
            result = current;
            if (index < 2) do {
                ((SavedGroups *)((u8 *)groups + index * 4))->reserve[0] = ((SavedGroups *)((u8 *)groups + index * 4))->reserve[1];
                index++;
            } while (index < 2);
            groups->reserve[2] = 0;
        }
    }
    return result;
}
void saved_record_features_observe(SavedRecord *record) {
    u8 features[64];
    u8 index;
    native_feature_collect(record->species, record->variant, (u8 *)record + 122, features);
    index = 0;
    do {
        native_feature_observed_set(features[index]);
        index++;
    } while (index < 64);
}
