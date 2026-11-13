typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u8 prefix[0x35D];
    u8 low : 2;
    u8 selection : 1;
    u8 high : 5;
    u8 tail[226];
} Actor;
extern Actor *ov001_side_slot_record_021db438(s32, s32);
void native_ov001_021dccd0(u32 word) {
    Actor *own;
    Actor *opposing;
    s32 index;
    u8 selected;
    own = ov001_side_slot_record_021db438(0, 0);
    opposing = ov001_side_slot_record_021db438(1, 0);
    selected = word;
    index = 0;
    do {
        own->selection = selected;
        opposing->selection = selected;
        index++;
        own++;
        opposing++;
    } while (index < 3);
}
