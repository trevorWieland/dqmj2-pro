typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {
    u8 control;
    u8 padding[6];
    u8 command[8];
} CardRegisters;
void saved_20261029_card_command(u32 first,u32 second) {
    volatile CardRegisters *const registers = (volatile CardRegisters *)0x040001a1;
    while (*(volatile u32 *)0x040001a4 & 0x80000000) {}
    registers->control = 0xc0;
    registers->command[0] = first >> 24;
    registers->command[1] = first >> 16;
    registers->command[2] = first >> 8;
    registers->command[3] = first;
    registers->command[4] = second >> 24;
    registers->command[5] = second >> 16;
    registers->command[6] = second >> 8;
    registers->command[7] = second;
}
