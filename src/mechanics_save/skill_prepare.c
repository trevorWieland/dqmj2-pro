typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 prefix[28]; u16 initial[6]; u8 tail[60]; } NativeEktRecord;
typedef struct { u16 values[8]; u8 level; u8 padding[7]; u32 next_word; u32 tail; } SavedBlock20;
typedef struct { u8 id; u8 allocated; } SavedSkill;
extern NativeEktRecord *native_ekt_record(int);
extern void native_fill(void *, u32, u32);
extern u32 native_level_word(int, int, int);
int saved_default_block20(int species, int variant, SavedBlock20 *block) {
    NativeEktRecord *kind = native_ekt_record(species);
    if (!block) return 0;
    native_fill(block, 0, 32);
    block->values[0] = kind->initial[0];
    block->values[1] = kind->initial[1];
    block->values[2] = kind->initial[0];
    block->values[3] = kind->initial[1];
    block->values[4] = kind->initial[2];
    block->values[5] = kind->initial[3];
    block->values[6] = kind->initial[4];
    block->values[7] = kind->initial[5];
    block->level = 1;
    block->next_word = native_level_word(species, variant, 2);
    return 1;
}
int saved_skill_ids_normalize(SavedSkill *skills, int count) {
    int index;
    int later;
    int any = 0;
    if (!skills || count < 1 || count > 5) return 0;
    index = 0;
    if (count > 0) do {
        if (skills[index].id) { any = 1; break; }
        index++;
    } while (index < count);
    if (!any) { skills[0].id = 142; return 1; }
    if (count < 2) return 1;
    index = 0;
    if (count - 1 > 0) do {
        later = index + 1;
        if (later < count) do {
            if (skills[index].id == skills[later].id) skills[later].id = 0;
            later++;
        } while (later < count);
        index++;
    } while (index < count - 1);
    index = 0;
    if (count - 1 > 0) do {
        u8 current = skills[index].id;
        if (!current) {
            later = index + 1;
            if (later < count) do {
                u8 next = skills[later].id;
                if (next) {
                    skills[later].id = current;
                    skills[index].id = next;
                    break;
                }
                later++;
            } while (later < count);
        }
        index++;
    } while (index < count - 1);
    return 1;
}
