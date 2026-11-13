typedef unsigned char u8;
typedef signed int s32;
extern u8 *ov001_side_slot_record_021db438(s32, s32);
extern void native_fn_02008e0c(const void *, void *, unsigned int);
void native_ov001_021dcabc(void) {
    u8 *own;
    s32 own_index;
    u8 *opposing;
    s32 opposing_index;
    own = ov001_side_slot_record_021db438(0, 0);
    own_index = 0;
    do {
        native_fn_02008e0c(own + 0x22C, own + 0x2A4, 120);
        own_index++;
        own[0x431] = 0;
        own += 1088;
    } while (own_index < 3);
    opposing = ov001_side_slot_record_021db438(1, 0);
    opposing_index = 0;
    do {
        native_fn_02008e0c(opposing + 0x22C, opposing + 0x2A4, 120);
        opposing_index++;
        opposing[0x431] = 0;
        opposing += 1088;
    } while (opposing_index < 3);
}
