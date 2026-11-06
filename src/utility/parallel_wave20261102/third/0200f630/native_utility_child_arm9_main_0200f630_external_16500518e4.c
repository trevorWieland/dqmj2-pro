typedef unsigned char u8;
typedef unsigned long u32;
typedef volatile u8 vu8;
typedef volatile u32 vu32;
    void native_utility_child_arm9_main_0200f630 (u32 cmd1, u32 cmd2)
    {
        while ((*(vu32 *)(0x04000000 + 0x1A4) & 0x80000000 ) != 0);
        *(vu8 *)(0x04000000 + 0x1A1) = 0x00 | 0x80 | 0x40 ;
        {
            vu8 *const p_cmd = (vu8 *)(0x04000000 + 0x1A8) ;
            p_cmd[0] = (u8)(cmd1 >> (8 * 3));
            p_cmd[1] = (u8)(cmd1 >> (8 * 2));
            p_cmd[2] = (u8)(cmd1 >> (8 * 1));
            p_cmd[3] = (u8)(cmd1 >> (8 * 0));
            p_cmd[4] = (u8)(cmd2 >> (8 * 3));
            p_cmd[5] = (u8)(cmd2 >> (8 * 2));
            p_cmd[6] = (u8)(cmd2 >> (8 * 1));
            p_cmd[7] = (u8)(cmd2 >> (8 * 0));
        }
    }
