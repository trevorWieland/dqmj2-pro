typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 prefix[4]; u16 variant_group:4; u16 other:12; u8 middle[57]; u8 innate[4]; u8 tail[33]; } NativeEktRecord;
typedef struct { u8 thresholds[10]; u8 middle[40]; u8 features[10]; } NativeSkillRecord;
typedef struct { u8 flags; u8 parent; u8 remaining[6]; } NativeFeatureRecord;
typedef struct { u32 magic; int count; } NativeFeatureHeader;
typedef struct { u32 reserved; NativeFeatureHeader *header; NativeFeatureRecord *records; } NativeFeatureState;
typedef struct { u8 skill; u8 allocated; } SavedSkill;
extern NativeFeatureState native_feature_state;
extern NativeEktRecord *saved_native_ekt_record(int);
extern int saved_native_category(int);
extern NativeSkillRecord *saved_native_skill_record(u32);
extern void native_fill(void *, u32, u32);
u32 saved_native_variant_offset(int id) {
    u32 result = 0;
    u8 group = saved_native_ekt_record(id)->variant_group;
    if (group) result = (u8)(((int)group - 1) / 3);
    return result;
}
int saved_feature_append_allowed(int feature, const u8 *list, int count) {
    int index;
    NativeFeatureRecord *records;
    int allowed;
    records = native_feature_state.records;
    index = feature * 8;
    allowed = 1;
    if (!(records[feature].flags & 4)) {
        NativeFeatureRecord *record = (NativeFeatureRecord *)((u8 *)records + index);
        int parent = record->parent;
        index = 0;
        if (count > 0) do {
            int current = list[index];
            if (current == feature || current == parent) {
                allowed = 0;
                break;
            }
            index++;
        } while (index < count);
    }
    return allowed;
}
int saved_feature_parent_find(int feature) {
    int count;
    int index;
    int result;
    NativeFeatureRecord *records;
    count = native_feature_state.header->count;
    result = 0;
    index = 0;
    if (count > 0) {
        records = native_feature_state.records;
        do {
            if (records[index].parent == feature) {
                result = index;
                break;
            }
            index++;
        } while (index < count);
    }
    return result;
}
int saved_feature_remove_first(int feature, u8 *list, int count) {
    int last;
    int index;
    int found;
    found = -1;
    index = 0;
    if (count > 0) do {
            if (list[index] == feature) {
                found = index;
                break;
            }
            index++;
        } while (index < count);
    if (found >= 0) {
        last = count - 1;
        if (found < last) do {
                u8 *source = list + found;
                list[found] = source[1];
                found++;
            } while (found < last);
        count--;
        list[count] = 0;
    }
    return count;
}
int saved_feature_collect(int species, int variant, SavedSkill *skills, u8 *output) {
    int index;
    int allocated;
    int feature;
    int count;
    NativeSkillRecord *skill_record;
    int slot;
    const u8 *innate;
    int maximum;
    native_fill(output, 0, 64);
    count = 0;
    innate = saved_native_ekt_record(species)->innate;
    switch (saved_native_category(species)) {
    case 0:
        if (variant + (int)saved_native_variant_offset(species) + 2 > 4) maximum = 4;
        else maximum = variant + (int)saved_native_variant_offset(species) + 2;
        break;
    case 1:
        if ((variant + (int)saved_native_variant_offset(species)) / 2 + 3 > 4) maximum = 4;
        else maximum = (variant + (int)saved_native_variant_offset(species)) / 2 + 3;
        break;
    case 2:
        maximum = 4;
        break;
    }
    {
        int initial_index = 0;
        if (maximum > 0) do {
            int initial_feature = *innate;
            if (initial_feature) {
                output[count] = initial_feature;
                count = count + 1;
            }
            initial_index++;
            innate++;
        } while (initial_index < maximum);
    }
    if (skills) {
        slot = 0;
        do {
            int skill_id = skills[slot].skill;
            if (skill_id > 0) {
                skill_record = saved_native_skill_record(skill_id);
                if (skill_record) {
                    allocated = skills[slot].allocated;
                    index = 0;
                    do {
                        u8 *entry = (u8 *)skill_record + index;
                        feature = entry[50];
                        if (feature > 0 && allocated >= entry[0] && saved_feature_append_allowed(feature, output, count)) {
                            int parent = saved_feature_parent_find(feature);
                            if (parent > 0) count = saved_feature_remove_first(parent, output, count);
                            output[count] = feature;
                            count = count + 1;
                        }
                        index++;
                    } while (index < 10);
                }
            }
            slot++;
        } while (slot < 5);
    }
    return count;
}
int saved_feature_occurrences(int feature, const u8 *list) {
    int index;
    int count = 0;
    if (list) {
        index = 0;
        do {
            int current = list[index];
            if (!current) break;
            if (current == feature) count++;
            index++;
        } while (index < 64);
    }
    return count;
}
