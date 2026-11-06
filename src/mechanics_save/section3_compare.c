typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef struct { u32 words[3]; } OpaqueSavedRecord12;
typedef struct { u32 words[19]; } OpaqueSavedRecord76;
extern int saved_section3_index_valid(int);
extern OpaqueSavedRecord12 *saved_section3_records12_pointer(void);
extern OpaqueSavedRecord76 *saved_section3_records76_pointer(void);
extern OpaqueSavedRecord76 *saved_section3_scratch_pointer(void);
extern void native_copy_words(const void *, void *, u32);
extern void native_copy(const void *, void *, u32);
int saved_section3_pair_reconcile(int first_index, int second_index) {
    if (saved_section3_index_valid(first_index) && saved_section3_index_valid(second_index)) {
        OpaqueSavedRecord12 *first_values = saved_section3_records12_pointer() + first_index;
        OpaqueSavedRecord12 *second_values = saved_section3_records12_pointer() + second_index;
        OpaqueSavedRecord76 *first_record = saved_section3_records76_pointer() + first_index;
        OpaqueSavedRecord76 *second_record = saved_section3_records76_pointer() + second_index;
        u64 first_sum = first_values->words[0] + first_values->words[1] + first_values->words[2];
        u64 second_sum = second_values->words[0] + second_values->words[1] + second_values->words[2];
        if (first_sum > second_sum) {
            native_copy_words(first_record, second_record, 76);
            native_copy_words(first_values, second_values, 12);
            return 1;
        }
        if (first_sum < second_sum) {
            native_copy_words(second_record, first_record, 76);
            native_copy_words(second_values, first_values, 12);
            return 1;
        }
    }
    return 0;
}
int saved_section3_scratch_read(void *output) {
    native_copy_words(saved_section3_scratch_pointer(), output, 76);
    return 1;
}
void *saved_section3_scratch_date_pointer(void) { return (u8 *)saved_section3_scratch_pointer() + 60; }
void saved_section3_scratch_date_write(const void *input) {
    native_copy(input, (u8 *)saved_section3_scratch_pointer() + 60, 16);
}
