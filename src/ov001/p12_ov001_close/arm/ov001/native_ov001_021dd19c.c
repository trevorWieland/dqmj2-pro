/* ov001 row 0x021dd19c: 2148 bytes.
 *
 * What it does: 503 instructions; 119 call(s) to 0x021dba58, 0x021dba58, 0x021dba58, +116 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 34 literal slot(s) in the extent
 *
 * Decoded shape: loop with 119 calls (503 instructions, 119 calls, 58 branches, 118 back edges, 34 literal slots).
 *
 *   pool +0x7dc -> native_data_0222eacc (image word 0x0222eacc)
 *   pool +0x7e0 -> native_data_0222ead4 (image word 0x0222ead4)
 *   pool +0x7e4 -> native_data_0222eadc (image word 0x0222eadc)
 *   pool +0x7e8 -> native_data_0222eae4 (image word 0x0222eae4)
 *   pool +0x7ec -> native_data_0222eaec (image word 0x0222eaec)
 *   pool +0x7f0 -> native_data_0222eaf4 (image word 0x0222eaf4)
 *   pool +0x7f4 -> native_data_0222eafc (image word 0x0222eafc)
 *   pool +0x7f8 -> native_data_0222eb04 (image word 0x0222eb04)
 *   pool +0x7fc -> native_data_0222eb0c (image word 0x0222eb0c)
 *   pool +0x800 -> native_data_0222eb14 (image word 0x0222eb14)
 *   pool +0x804 -> native_data_0222eb1c (image word 0x0222eb1c)
 *   pool +0x808 -> native_data_0222eb24 (image word 0x0222eb24)
 *   pool +0x80c -> native_data_0222eb2c (image word 0x0222eb2c)
 *   pool +0x810 -> native_fn_021e9178 (image word 0x021e9178)
 *   pool +0x814 -> native_data_0222eb34 (image word 0x0222eb34)
 *   pool +0x818 -> native_data_0222eb3c (image word 0x0222eb3c)
 *   pool +0x81c -> native_data_0222eb44 (image word 0x0222eb44)
 *   pool +0x820 -> native_data_0222eb4c (image word 0x0222eb4c)
 *   pool +0x824 -> native_data_0222eb54 (image word 0x0222eb54)
 *   pool +0x828 -> native_data_0222eb5c (image word 0x0222eb5c)
 *   pool +0x82c -> native_data_0222eb64 (image word 0x0222eb64)
 *   pool +0x830 -> native_data_0222eb6c (image word 0x0222eb6c)
 *   pool +0x834 -> native_data_0222eb74 (image word 0x0222eb74)
 *   pool +0x838 -> native_data_0222eb7c (image word 0x0222eb7c)
 *   pool +0x83c -> native_data_0222eb84 (image word 0x0222eb84)
 *   pool +0x840 -> native_data_0222eb8c (image word 0x0222eb8c)
 *   pool +0x844 -> native_data_0222eb94 (image word 0x0222eb94)
 *   pool +0x848 -> native_data_0222eb9c (image word 0x0222eb9c)
 *   pool +0x84c -> native_data_0222eba4 (image word 0x0222eba4)
 *   pool +0x850 -> native_data_0222ebac (image word 0x0222ebac)
 *   pool +0x854 -> native_data_0222ebb4 (image word 0x0222ebb4)
 *   pool +0x858 -> native_data_0222ebbc (image word 0x0222ebbc)
 *   pool +0x85c -> native_data_0222ebc4 (image word 0x0222ebc4)
 *   pool +0x860 -> native_data_0222ebcc (image word 0x0222ebcc)
 *   branch +0xa0 -> +0xc0
 *   branch +0xbc -> +0x124
 *   branch +0xc4 -> +0xdc
 *   branch +0xd8 -> +0x124
 *   branch +0xe0 -> +0xf8
 *   branch +0xf4 -> +0x124
 *   branch +0x104 -> +0x118
 *   branch +0x114 -> +0x124
 *   branch +0x140 -> +0x160
 *   branch +0x15c -> +0x1bc
 *   branch +0x164 -> +0x184
 *   branch +0x180 -> +0x1bc
 *   branch +0x190 -> +0x1a0
 *   branch +0x19c -> +0x1bc
 *   branch +0x1a4 -> +0x1b4
 *   branch +0x1b0 -> +0x1bc
 *   branch +0x1cc -> +0x1ec
 *   branch +0x1e8 -> +0x248
 *   branch +0x1f0 -> +0x210
 *   branch +0x20c -> +0x248
 *   branch +0x21c -> +0x22c
 *   branch +0x228 -> +0x248
 *   branch +0x230 -> +0x240
 *   branch +0x23c -> +0x248
 *   branch +0x250 -> +0x270
 *   branch +0x278 -> +0x298
 *   branch +0x2a0 -> +0x2c0
 *   branch +0x2c4 -> +0x2ec
 *   branch +0x2f0 -> +0x318
 *   branch +0x338 -> +0x358
 *   branch +0x360 -> +0x380
 *   branch +0x388 -> +0x3a8
 *   branch +0x3b0 -> +0x3d0
 *   branch +0x3d8 -> +0x3f8
 *   branch +0x400 -> +0x420
 *   branch +0x424 -> +0x44c
 *   branch +0x450 -> +0x478
 *   branch +0x47c -> +0x4a4
 *   branch +0x4a8 -> +0x4d0
 *   branch +0x4d4 -> +0x4f4
 *   branch +0x4f8 -> +0x518
 *   branch +0x51c -> +0x544
 *   branch +0x548 -> +0x568
 *   branch +0x56c -> +0x58c
 *   branch +0x590 -> +0x5b8
 *   branch +0x5bc -> +0x5dc
 *   branch +0x5e0 -> +0x600
 *   branch +0x604 -> +0x62c
 *   branch +0x630 -> +0x650
 *   branch +0x654 -> +0x674
 *   branch +0x678 -> +0x6a0
 *   branch +0x6a8 -> +0x6c8
 *   branch +0x6d0 -> +0x6f0
 *   branch +0x6f8 -> +0x718
 *   branch +0x71c -> +0x744
 *   branch +0x748 -> +0x770
 *   branch +0x780 -> +0x7a0
 *   branch +0x7ac -> +0x7bc
 *   branch +0x7c0 -> +0x7d0
 *   test +0x9c cmp r10, #0
 *   test +0xc0 cmp r4, #0
 *   test +0xdc cmp r6, #0
 *   test +0xfc cmp r0, #2
 *   test +0x13c cmp r9, #0
 *   test +0x160 cmp r10, #0
 *   test +0x184 cmp r4, #0
 *   test +0x1a0 cmp r6, #0
 *   test +0x1c8 cmp r10, #0
 *   test +0x1ec cmp r9, #0
 *   test +0x210 cmp r4, #0
 *   test +0x22c cmp r6, #0
 *   test +0x248 cmp r7, #0
 *   test +0x24c cmpeq r8, #0
 *   test +0x270 cmp r5, #0
 *   test +0x274 cmpeq r6, #0
 *   test +0x298 cmp r11, #0
 *   test +0x29c cmpeq r4, #0
 *   test +0x2c0 cmp r10, #0
 *   test +0x2ec cmp r9, #0
 *   test +0x330 cmp r7, #0
 *   test +0x334 cmpeq r8, #0
 *   test +0x358 cmp r5, #0
 *   test +0x35c cmpeq r6, #0
 *   test +0x380 cmp r11, #0
 *   test +0x384 cmpeq r4, #0
 *   test +0x3a8 cmp r7, #0
 *   test +0x3ac cmpeq r8, #0
 *   test +0x3d0 cmp r5, #0
 *   test +0x3d4 cmpeq r6, #0
 *   test +0x3f8 cmp r11, #0
 *   test +0x3fc cmpeq r4, #0
 *   test +0x420 cmp r10, #0
 *   test +0x44c cmp r9, #0
 *   test +0x478 cmp r9, #0
 *   test +0x4a4 cmp r10, #0
 *   test +0x4d0 cmp r7, #0
 *   test +0x4f4 cmp r5, #0
 *   test +0x518 cmp r9, #0
 *   test +0x544 cmp r8, #0
 *   test +0x568 cmp r6, #0
 *   test +0x58c cmp r10, #0
 *   test +0x5b8 cmp r7, #0
 *   test +0x5dc cmp r5, #0
 *   test +0x600 cmp r9, #0
 *   test +0x62c cmp r8, #0
 *   test +0x650 cmp r6, #0
 *   test +0x674 cmp r10, #0
 *   test +0x6a0 cmp r7, #0
 *   test +0x6a4 cmpeq r8, #0
 *   test +0x6c8 cmp r5, #0
 *   test +0x6cc cmpeq r6, #0
 *   test +0x6f0 cmp r11, #0
 *   test +0x6f4 cmpeq r4, #0
 *   test +0x718 cmp r10, #0
 *   test +0x744 cmp r9, #0
 *   test +0x77c cmp r10, #0
 *   test +0x7a0 cmp r4, #0
 *   test +0x7bc cmp r6, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dd19c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021dba58(void);
extern void native_fn_021dbac8(void);
extern void native_fn_021db530(void);
extern void native_fn_021d732c(void);
extern void native_fn_021d7d4c(void);
extern void native_fn_021d7564(void);
extern u8 native_data_0222eacc[];
extern u8 native_data_0222ead4[];
extern u8 native_data_0222eadc[];
extern u8 native_data_0222eae4[];
extern void native_fn_021d76ec(void);
extern u8 native_data_0222eaec[];
extern u8 native_data_0222eaf4[];
extern u8 native_data_0222eafc[];
extern u8 native_data_0222eb04[];
extern u8 native_data_0222eb0c[];
extern u8 native_data_0222eb14[];
extern u8 native_data_0222eb1c[];
extern u8 native_data_0222eb24[];
extern u8 native_data_0222eb2c[];
extern void native_fn_021e9178(void);
extern void native_fn_021d7d00(void);
extern u8 native_data_0222eb34[];
extern u8 native_data_0222eb3c[];
extern u8 native_data_0222eb44[];
extern u8 native_data_0222eb4c[];
extern u8 native_data_0222eb54[];
extern u8 native_data_0222eb5c[];
extern u8 native_data_0222eb64[];
extern u8 native_data_0222eb6c[];
extern u8 native_data_0222eb74[];
extern u8 native_data_0222eb7c[];
extern u8 native_data_0222eb84[];
extern u8 native_data_0222eb8c[];
extern u8 native_data_0222eb94[];
extern u8 native_data_0222eb9c[];
extern u8 native_data_0222eba4[];
extern u8 native_data_0222ebac[];
extern u8 native_data_0222ebb4[];
extern u8 native_data_0222ebbc[];
extern u8 native_data_0222ebc4[];
extern u8 native_data_0222ebcc[];


asm u32 native_ov001_021dd19c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r0, #0
    mov r1, #2
    bl native_fn_021dba58
    mov r11, r0
    mov r0, #1
    mov r1, #2
    bl native_fn_021dba58
    mov r4, r0
    mov r0, #0
    mov r1, #1
    bl native_fn_021dba58
    mov r5, r0
    mov r0, #1
    mov r1, r0
    bl native_fn_021dba58
    mov r6, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_021dba58
    mov r7, r0
    mov r0, #1
    mov r1, #0
    bl native_fn_021dba58
    mov r8, r0
    mov r0, #0
    bl native_fn_021dbac8
    mov r9, r0
    mov r0, #1
    bl native_fn_021dbac8
    mov r10, r0
    mov r0, #0
    bl native_fn_021db530
    mov r0, #1
    bl native_fn_021db530
    str r0, [sp]
    mov r0, #2
    mov r1, r0
    bl native_fn_021d732c
    cmp r10, #0
    beq ov001_021dd19c_Lc0
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #2
    mov r2, #3
    bl native_fn_021d7564
    b ov001_021dd19c_L124
ov001_021dd19c_Lc0:
    cmp r4, #0
    beq ov001_021dd19c_Ldc
    ldr r1, =native_data_0222eacc
    mov r0, #2
    mov r2, #3
    bl native_fn_021d7564
    b ov001_021dd19c_L124
ov001_021dd19c_Ldc:
    cmp r6, #0
    beq ov001_021dd19c_Lf8
    ldr r1, =native_data_0222ead4
    mov r0, #2
    mov r2, #3
    bl native_fn_021d7564
    b ov001_021dd19c_L124
ov001_021dd19c_Lf8:
    ldr r0, [sp]
    cmp r0, #2
    mov r0, #2
    blt ov001_021dd19c_L118
    ldr r1, =native_data_0222eadc
    mov r2, #3
    bl native_fn_021d7564
    b ov001_021dd19c_L124
ov001_021dd19c_L118:
    ldr r1, =native_data_0222eae4
    mov r2, #16
    bl native_fn_021d7564
ov001_021dd19c_L124:
    mov r0, #2
    mov r1, #1
    bl native_fn_021d76ec
    mov r0, #3
    mov r1, #2
    bl native_fn_021d732c
    cmp r9, #0
    beq ov001_021dd19c_L160
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #3
    mov r2, #4
    bl native_fn_021d7564
    b ov001_021dd19c_L1bc
ov001_021dd19c_L160:
    cmp r10, #0
    beq ov001_021dd19c_L184
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #3
    mov r2, #4
    bl native_fn_021d7564
    b ov001_021dd19c_L1bc
ov001_021dd19c_L184:
    cmp r4, #0
    mov r0, #3
    mov r2, #4
    beq ov001_021dd19c_L1a0
    ldr r1, =native_data_0222eaec
    bl native_fn_021d7564
    b ov001_021dd19c_L1bc
ov001_021dd19c_L1a0:
    cmp r6, #0
    beq ov001_021dd19c_L1b4
    ldr r1, =native_data_0222eaf4
    bl native_fn_021d7564
    b ov001_021dd19c_L1bc
ov001_021dd19c_L1b4:
    ldr r1, =native_data_0222eafc
    bl native_fn_021d7564
ov001_021dd19c_L1bc:
    mov r0, #4
    mov r1, #2
    bl native_fn_021d732c
    cmp r10, #0
    beq ov001_021dd19c_L1ec
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #4
    mov r2, #5
    bl native_fn_021d7564
    b ov001_021dd19c_L248
ov001_021dd19c_L1ec:
    cmp r9, #0
    beq ov001_021dd19c_L210
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #4
    mov r2, #5
    bl native_fn_021d7564
    b ov001_021dd19c_L248
ov001_021dd19c_L210:
    cmp r4, #0
    mov r0, #4
    mov r2, #5
    beq ov001_021dd19c_L22c
    ldr r1, =native_data_0222eb04
    bl native_fn_021d7564
    b ov001_021dd19c_L248
ov001_021dd19c_L22c:
    cmp r6, #0
    beq ov001_021dd19c_L240
    ldr r1, =native_data_0222eb0c
    bl native_fn_021d7564
    b ov001_021dd19c_L248
ov001_021dd19c_L240:
    ldr r1, =native_data_0222eb14
    bl native_fn_021d7564
ov001_021dd19c_L248:
    cmp r7, #0
    cmpeq r8, #0
    beq ov001_021dd19c_L270
    mov r0, #5
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb1c
    mov r0, #5
    mov r2, #6
    bl native_fn_021d7564
ov001_021dd19c_L270:
    cmp r5, #0
    cmpeq r6, #0
    beq ov001_021dd19c_L298
    mov r0, #6
    mov r1, #2
    bl native_fn_021d732c
    mov r0, #6
    ldr r1, =native_data_0222eb24
    mov r2, r0
    bl native_fn_021d7564
ov001_021dd19c_L298:
    cmp r11, #0
    cmpeq r4, #0
    beq ov001_021dd19c_L2c0
    mov r0, #7
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb2c
    mov r0, #7
    mov r2, #6
    bl native_fn_021d7564
ov001_021dd19c_L2c0:
    cmp r10, #0
    beq ov001_021dd19c_L2ec
    mov r0, #8
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #8
    mov r2, #6
    bl native_fn_021d7564
ov001_021dd19c_L2ec:
    cmp r9, #0
    beq ov001_021dd19c_L318
    mov r0, #9
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #9
    mov r2, #6
    bl native_fn_021d7564
ov001_021dd19c_L318:
    mov r0, #13
    mov r1, #1
    bl native_fn_021d732c
    ldr r1, =native_fn_021e9178
    mov r0, #13
    bl native_fn_021d7d00
    cmp r7, #0
    cmpeq r8, #0
    beq ov001_021dd19c_L358
    mov r0, #10
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb34
    mov r0, #10
    mov r2, #13
    bl native_fn_021d7564
ov001_021dd19c_L358:
    cmp r5, #0
    cmpeq r6, #0
    beq ov001_021dd19c_L380
    mov r0, #11
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb3c
    mov r0, #11
    mov r2, #13
    bl native_fn_021d7564
ov001_021dd19c_L380:
    cmp r11, #0
    cmpeq r4, #0
    beq ov001_021dd19c_L3a8
    mov r0, #12
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb44
    mov r0, #12
    mov r2, #13
    bl native_fn_021d7564
ov001_021dd19c_L3a8:
    cmp r7, #0
    cmpeq r8, #0
    beq ov001_021dd19c_L3d0
    mov r0, #14
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb4c
    mov r0, #14
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L3d0:
    cmp r5, #0
    cmpeq r6, #0
    beq ov001_021dd19c_L3f8
    mov r0, #15
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb54
    mov r0, #15
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L3f8:
    cmp r11, #0
    cmpeq r4, #0
    beq ov001_021dd19c_L420
    mov r0, #16
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb5c
    mov r0, #16
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L420:
    cmp r10, #0
    beq ov001_021dd19c_L44c
    mov r0, #17
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #17
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L44c:
    cmp r9, #0
    beq ov001_021dd19c_L478
    mov r0, #18
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #18
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L478:
    cmp r9, #0
    beq ov001_021dd19c_L4a4
    mov r0, #19
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #19
    mov r2, #17
    bl native_fn_021d7564
ov001_021dd19c_L4a4:
    cmp r10, #0
    beq ov001_021dd19c_L4d0
    mov r0, #20
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #20
    mov r2, #17
    bl native_fn_021d7564
ov001_021dd19c_L4d0:
    cmp r7, #0
    beq ov001_021dd19c_L4f4
    mov r0, #30
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb64
    mov r0, #30
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L4f4:
    cmp r5, #0
    beq ov001_021dd19c_L518
    mov r0, #31
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb6c
    mov r0, #31
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L518:
    cmp r9, #0
    beq ov001_021dd19c_L544
    mov r0, #33
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #33
    mov r2, #15
    bl native_fn_021d7564
ov001_021dd19c_L544:
    cmp r8, #0
    beq ov001_021dd19c_L568
    mov r0, #26
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb74
    mov r0, #26
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L568:
    cmp r6, #0
    beq ov001_021dd19c_L58c
    mov r0, #27
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb7c
    mov r0, #27
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L58c:
    cmp r10, #0
    beq ov001_021dd19c_L5b8
    mov r0, #29
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #29
    mov r2, #15
    bl native_fn_021d7564
ov001_021dd19c_L5b8:
    cmp r7, #0
    beq ov001_021dd19c_L5dc
    mov r0, #38
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb84
    mov r0, #38
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L5dc:
    cmp r5, #0
    beq ov001_021dd19c_L600
    mov r0, #39
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb8c
    mov r0, #39
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L600:
    cmp r9, #0
    beq ov001_021dd19c_L62c
    mov r0, #41
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #41
    mov r2, #14
    bl native_fn_021d7564
ov001_021dd19c_L62c:
    cmp r8, #0
    beq ov001_021dd19c_L650
    mov r0, #34
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb94
    mov r0, #34
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L650:
    cmp r6, #0
    beq ov001_021dd19c_L674
    mov r0, #35
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eb9c
    mov r0, #35
    mov r2, #8
    bl native_fn_021d7564
ov001_021dd19c_L674:
    cmp r10, #0
    beq ov001_021dd19c_L6a0
    mov r0, #37
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #37
    mov r2, #14
    bl native_fn_021d7564
ov001_021dd19c_L6a0:
    cmp r7, #0
    cmpeq r8, #0
    beq ov001_021dd19c_L6c8
    mov r0, #21
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222eba4
    mov r0, #21
    mov r2, #9
    bl native_fn_021d7564
ov001_021dd19c_L6c8:
    cmp r5, #0
    cmpeq r6, #0
    beq ov001_021dd19c_L6f0
    mov r0, #22
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222ebac
    mov r0, #22
    mov r2, #9
    bl native_fn_021d7564
ov001_021dd19c_L6f0:
    cmp r11, #0
    cmpeq r4, #0
    beq ov001_021dd19c_L718
    mov r0, #23
    mov r1, #2
    bl native_fn_021d732c
    ldr r1, =native_data_0222ebb4
    mov r0, #23
    mov r2, #9
    bl native_fn_021d7564
ov001_021dd19c_L718:
    cmp r10, #0
    beq ov001_021dd19c_L744
    mov r0, #24
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #24
    mov r2, #9
    bl native_fn_021d7564
ov001_021dd19c_L744:
    cmp r9, #0
    beq ov001_021dd19c_L770
    mov r0, #25
    mov r1, #2
    bl native_fn_021d732c
    mov r0, r9
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #25
    mov r2, #9
    bl native_fn_021d7564
ov001_021dd19c_L770:
    mov r0, #43
    mov r1, #2
    bl native_fn_021d732c
    cmp r10, #0
    beq ov001_021dd19c_L7a0
    mov r0, r10
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #43
    mov r2, #12
    bl native_fn_021d7564
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021dd19c_L7a0:
    cmp r4, #0
    mov r0, #43
    mov r2, #12
    beq ov001_021dd19c_L7bc
    ldr r1, =native_data_0222ebbc
    bl native_fn_021d7564
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021dd19c_L7bc:
    cmp r6, #0
    beq ov001_021dd19c_L7d0
    ldr r1, =native_data_0222ebc4
    bl native_fn_021d7564
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_021dd19c_L7d0:
    ldr r1, =native_data_0222ebcc
    bl native_fn_021d7564
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
