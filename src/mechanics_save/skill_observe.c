typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 threshold[10]; u8 actions[40]; u8 features[10]; } NativeSkillRecord;
extern NativeSkillRecord *saved_native_skill_record(u32);
extern int saved_native_category(int);
extern int native_skill_event16_get(void);
extern int native_skill_raw_observed_set(int);
extern int native_skill_raw_level_get(int);
extern int native_skill_raw_level_set(int, u32);
extern int native_skill_entry_is_action(NativeSkillRecord *, signed char);
extern int native_feature_raw_observed_set(int);
extern int native_record_growth_type(int, int);
extern u8 native_level_filename[];
extern u32 native_level_word;
extern struct { u32 reserved[2]; u32 value; } native_level_result;
extern int native_resource_read(const void *, void *, u32, u32);
int saved_skill_threshold_prefix_count(NativeSkillRecord *record, int allocated) {
    int index = 0;
    do {
        if (record->actions[index * 4] == 0 && record->features[index] == 0) break;
        if (record->threshold[index] > allocated) break;
        index++;
    } while (index < 10);
    return index;
}
int saved_skill_entry_native_id(NativeSkillRecord *record, signed char index) {
    u8 *actions = record->actions + index * 4;
    u8 *features = record->features;
    int action = *actions;
    if (action == 0) action = features[index];
    return action;
}
void saved_skill_observe(int species, int skill, int allocated) {
    NativeSkillRecord *record = saved_native_skill_record(skill);
    int index;
    int count;
    if (saved_native_category(species) == 2) {
        if (!native_skill_event16_get()) return;
    }
    native_skill_raw_observed_set(skill);
    if (!record) return;
    count = (u8)saved_skill_threshold_prefix_count(record, allocated);
    if (native_skill_raw_level_get(skill) < count) native_skill_raw_level_set(skill, count);
    index = 0;
    if (count > 0) do {
        if (native_skill_entry_is_action(record, index) == 0) {
            int feature = saved_skill_entry_native_id(record, index);
            native_feature_raw_observed_set(feature);
        }
        index++;
    } while (index < count);
}
u32 saved_record_level_word(int species, int variant, int level) {
    u32 value;
    int index;
    index = level - 1;
    value = 0;
    if ((u32)index <= 99) {
        int category = native_record_growth_type(species, variant);
        u32 offset = category * 400 + index * 4;
        if (native_resource_read(native_level_filename, &native_level_word, 4, offset)) value = native_level_result.value;
    }
    return value;
}
