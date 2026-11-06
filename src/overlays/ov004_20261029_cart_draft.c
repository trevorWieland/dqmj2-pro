typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
#define IO8(a) (*(volatile u8 *)(a))
#define IO16(a) (*(volatile u16 *)(a))
#define IO32(a) (*(volatile u32 *)(a))
extern u32 func_020060e4(void);
extern void func_0200613c(u32);
extern u32 func_020102c4(u32);
extern void func_020102e0(u32);
extern u32 func_0201109c(s32, u32, void *, u32, u32, u32, u32);
extern u32 func_ov004_021d83d4(void *, u32);
static inline void read_card(void *buffer, u32 sector, s32 length) {
    u8 saved_command[8];
    u16 old_exmem;
    s32 control;
    s32 offset;

    s32 index;
    u32 address;

    u32 word;
    u32 io_base;
    volatile u8 *absolute_base;
    volatile u8 *command_base;
    io_base = 1;
    io_base <<= 26;
    command_base = (volatile u8 *)0x04000000;
    absolute_base = (volatile u8 *)0;
    old_exmem = IO16(0x04000204);
    IO16(0x04000204) &= ~0x800;
    control = 5;
    control += IO8(io_base + 0x4000) & 1;
    control <<= 18;
    control -= 13;
    control <<= 5;
    control = IO32(control);
    control = (control & ~0x07000000) | 0xA1000000;
    offset = -(s32)(sector & 0x1FF);
    while (IO32(io_base + 0x1A4) & 0x80000000) {
    }

    IO8(io_base + 0x1A1) = 0x80;
    index = 0;
    do {
        saved_command[index] = *(absolute_base + 0x040001A8 + index);
        index++;
    } while (index < 8);
    address = sector + offset;
    if (offset < length) {
        do {
        command_base[0x1a8] = 0xB7;
        command_base[0x1a9] = address >> 24;
        command_base[0x1aa] = address >> 16;
        command_base[0x1ab] = address >> 8;
        command_base[0x1ac] = address;
        command_base[0x1ad] = 0;
        command_base[0x1ae] = 0;
        command_base[0x1af] = 0;
        IO32(io_base + 0x1A4) = control;
        do {
            if (IO32(io_base + 0x1A4) & 0x00800000) {
            word = IO32(io_base + 0x100010);
            if (offset >= 0 && offset < length) {
                *(u32 *)((u32)buffer + offset) = word;
            }
            offset += 4;
            }
        } while (IO32(io_base + 0x1A4) & 0x80000000);
        address += 512;
        } while (offset < length);
    }

    index = 0;
    do {
        *(absolute_base + 0x040001A8 + index) = saved_command[index];
        index++;
    } while (index < 8);
    IO16(io_base + 0x204) = old_exmem;
}
u32 native_ov004_021d8410(void) {
    u32 crcs[7];
    u8 buffer[512];
    s32 trial;
    u32 sector;
    u16 lock_id;
    u32 factor;

    s32 clear_index;
    sector = 0x1000;
    lock_id = func_020060e4();
    func_020102c4(lock_id);
    trial = 0;
    do {
        read_card(buffer, sector, 512);
        crcs[trial] = func_ov004_021d83d4(buffer, 512);
        func_0201109c(-1, sector + 0x7000, buffer, 512, 0, 0, 0);
        crcs[trial + 3] = func_ov004_021d83d4(buffer, 512);
        trial++;
        sector += 512;
    } while (trial < 3);
    func_020102e0(lock_id);
    func_0200613c(lock_id);
    trial = 0;
    do {
        if (crcs[3] != crcs[trial]) {
            factor = 251;
            goto clear;
        }
        trial++;
    } while (trial < 3);
    if (crcs[3] == crcs[4] && crcs[3] == crcs[5]) {
        factor = 251;
    } else {
        factor = 241;
    }
clear:
    clear_index = 0;
    do {
        ((u32 *)buffer)[clear_index] = clear_index;
        clear_index++;
    } while (clear_index < 128);
    return factor * 179;
}
u32 native_ov004_021d8650(void) {
    u32 crcs[7];
    u8 buffer[512];
    s32 trial;
    u32 sector;
    u16 lock_id;
    u32 factor;

    s32 clear_index;
    sector = 0x1000;
    lock_id = func_020060e4();
    func_020102c4(lock_id);
    trial = 0;
    do {
        read_card(buffer, sector, 512);
        crcs[trial] = func_ov004_021d83d4(buffer, 512);
        func_0201109c(-1, sector + 0x7000, buffer, 512, 0, 0, 0);
        crcs[trial + 3] = func_ov004_021d83d4(buffer, 512);
        trial++;
        sector += 512;
    } while (trial < 3);
    func_020102e0(lock_id);
    func_0200613c(lock_id);
    trial = 0;
    do {
        if (crcs[3] != crcs[trial]) {
            factor = 241;
            goto clear;
        }
        trial++;
    } while (trial < 3);
    if (crcs[3] == crcs[4] && crcs[3] == crcs[5]) {
        factor = 241;
    } else {
        factor = 251;
    }
clear:
    clear_index = 0;
    do {
        ((u32 *)buffer)[clear_index] = clear_index;
        clear_index++;
    } while (clear_index < 128);
    return factor * 191;
}
