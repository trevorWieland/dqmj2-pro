typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 flags; void *record; } Candidate;
extern u8 data_020fbae8[];
Candidate *native_main_0204854c(u32 bank, u32 record_index) {
    u32 offset;
    Candidate *candidates;
    u8 index;
    u32 base;
    offset = bank * 0x3744;
    base = offset + (u32)data_020fbae8;
    candidates = (Candidate *)(base + 0x320);
    index = 0;
    do {
        Candidate *candidate = &candidates[index];
        if ((candidate->flags & 1) != 1) {
            candidate->record = (void *)(base + record_index * 100);
            candidate->flags |= 1;
            return candidate;
        }
        index++;
    } while (index < 128);
    return 0;
}
