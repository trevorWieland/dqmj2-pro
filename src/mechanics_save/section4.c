typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 prefix[43]; u8 before_mode[3]; u8 mode; u8 middle[0x1ab]; u8 flags; u8 tail[12]; } OpaqueSavedRecord;
typedef struct { u8 count; u8 prefix[79]; OpaqueSavedRecord records[]; } OpaqueSavedSection4;
extern OpaqueSavedSection4 *saved_section4_pointer(void);
extern OpaqueSavedRecord native_section4_current_record;
extern struct { u8 prefix[4]; u8 selected; } native_section4_selection;
extern u8 native_section4_halfwords[];
extern void native_copy(const void *, void *, u32);
extern void native_fill(void *, u32, u32);
extern u32 native_section4_mode_get(void);
void saved_section4_current_set(const OpaqueSavedRecord *record, u32 mode) {
    saved_section4_pointer();
    native_copy(record, &native_section4_current_record, sizeof(OpaqueSavedRecord));
    native_section4_current_record.mode = mode;
}
void saved_section4_current_halfword_set(int index, u32 value) {
    *(u16 *)(native_section4_halfwords + index * 0x84) = value;
}
int saved_section4_append(void) {
    OpaqueSavedSection4 *section = saved_section4_pointer();
    if (native_section4_current_record.mode >= 7) return 0;
    if (section->count == 8) return 0;
    native_copy(&native_section4_current_record, &section->records[section->count], sizeof(OpaqueSavedRecord));
    if (native_section4_mode_get() == 3) {
        section->records[(u32)section->count].flags |= 1;
        section->records[(u32)section->count].flags |= 2;
    }
    if (native_section4_mode_get() == 0) section->records[(u32)section->count].flags |= 2;
    section->count++;
    return 1;
}
void saved_section4_read(int index, OpaqueSavedRecord *record) {
    OpaqueSavedSection4 *section = saved_section4_pointer();
    native_copy(&section->records[index], record, sizeof(OpaqueSavedRecord));
    native_section4_selection.selected = index;
}
void saved_section4_remove(int index) {
    OpaqueSavedSection4 *section = saved_section4_pointer();
    u32 input;
    u32 output;
    u8 remaining;
    native_fill(&section->records[index], 0, sizeof(OpaqueSavedRecord));
    output = 0;
    input = 0;
    if (input < section->count) do {
            if (section->records[input].mode) {
                section->records[output] = section->records[input];
                output = (u8)(output + 1);
            }
            input = (u8)(input + 1);
        } while (input < section->count);
    section->count = (u16)output;
    remaining = output;
    if (remaining < 8) do {
            native_fill(&section->records[remaining], 0, sizeof(OpaqueSavedRecord));
            remaining++;
        } while (remaining < 8);
}
void saved_section4_selected_flags_update(void) {
    OpaqueSavedSection4 *section = saved_section4_pointer();
    if (native_section4_mode_get() == 3) {
        section->records[(u32)native_section4_selection.selected].flags |= 1;
        section->records[(u32)native_section4_selection.selected].flags |= 2;
    }
    if (native_section4_mode_get() == 0) section->records[(u32)native_section4_selection.selected].flags |= 2;
}
