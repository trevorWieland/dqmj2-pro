/* Display-control setup sequence.
 *
 * Programs the main engine's display control word, two scroll registers, two
 * backdrop/OBJ window registers and finally the display mode bits. The image
 * reads the control word twice and keeps the base in one register, so the block
 * is a register file at 0x04000000 rather than separate absolute writes.
 * Unknowns: why the 0x44 value is 0x14bf and which engine state this expects.
 */
typedef unsigned short u16;
typedef unsigned int u32;

#define REG32(address) (*(volatile u32 *)(address))
#define REG16(address) (*(volatile u16 *)(address))

void native_ov000_02223328(void)
{
    REG32(0x04000000) = (REG32(0x04000000) & ~0x1f00) | 0xa00;
    REG16(0x04000048) = (REG16(0x04000048) & ~0x3f) | 0x28;
    REG16(0x0400004a) = (REG16(0x0400004a) & ~0x3f) | 0x2a;
    REG16(0x04000040) = 0xff;
    REG16(0x04000044) = 0x14bf;
    REG32(0x04000000) = (REG32(0x04000000) & ~0xe000) | 0x2000;
}
