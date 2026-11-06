typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { u8 id; u8 inputs[3]; } NativeSkillAction;
typedef struct { u8 threshold[10]; NativeSkillAction actions[10]; u8 features[10]; } NativeSkillRecord;
u32 native_main_0207adb0(NativeSkillRecord *record, s8 index, int member) {
    NativeSkillAction *entry = record->actions + index;
    if (entry->id != 0) return entry->inputs[member];
    return (u32)record;
}
