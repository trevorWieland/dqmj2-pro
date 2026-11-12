/* ov001 row 0x021fd1b8: 208 bytes.
 *
 * What it does: 49 instructions; 12 call(s) to 0x02202120, 0x021fd22c, 0x021fd22c, +9 more; loops (back edge at +0x80); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (49 instructions, 13 calls, 11 branches, 4 back edges, 3 literal slots).
 *
 *   pool +0xc4 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0xc8 -> native_data_0222edd0 (image word 0x0222edd0)
 *   pool +0xcc -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x30 -> +0x54
 *   branch +0x34 -> +0x84
 *   branch +0x3c -> +0x74
 *   branch +0x44 -> +0x74
 *   branch +0x4c -> +0x84
 *   branch +0x50 -> +0x74
 *   branch +0x58 -> +0x74
 *   branch +0x60 -> +0x74
 *   branch +0x68 -> +0x74
 *   branch +0x70 -> +0x84
 *   branch +0x98 -> +0xa8
 *   back edge +0x9c -> +0x00
 *   branch +0xa4 -> +0xbc
 *   branch +0xb0 -> +0xbc
 *   test +0x2c cmp r0, #9
 *   test +0x38 cmp r0, #1
 *   test +0x40 cmp r0, #0
 *   test +0x48 cmpne r0, #1
 *   test +0x54 cmp r0, #14
 *   test +0x5c cmp r0, #13
 *   test +0x64 cmpne r0, #14
 *   test +0x94 cmp r5, #2
 *   test +0xa8 cmp r5, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd1b8; the literal pool and
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

extern u8 native_data_0222edd0[];
extern void native_fn_02202120(void);
extern void native_fn_022040f8(void);
extern void native_fn_0220412c(void);
extern void native_fn_02204168(void);
extern void native_fn_021fd178(void);
extern void native_fn_02202230(void);
extern void native_fn_020851d4(void);
extern void native_fn_02085200(void);


asm u32 native_ov001_021fd1b8 (register u32 a0)
{
ov001_021fd1b8_L0:
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x02239c10
    ldr r1, =native_data_0222edd0
    ldrb r0, [r0, #0xa]
    mov r4, #0
    ldr r0, [r1, r0, lsl #2]
    blx r0
    mov r5, r0
    bl native_fn_02202120
    ldr r0, =0x02239c10
    ldrb r0, [r0, #0xa]
    cmp r0, #9
    bgt ov001_021fd1b8_L54
    bge ov001_021fd1b8_L84
    cmp r0, #1
    bgt ov001_021fd1b8_L74
    cmp r0, #0
    blt ov001_021fd1b8_L74
    cmpne r0, #1
    beq ov001_021fd1b8_L84
    b ov001_021fd1b8_L74
ov001_021fd1b8_L54:
    cmp r0, #14
    bgt ov001_021fd1b8_L74
    cmp r0, #13
    blt ov001_021fd1b8_L74
    cmpne r0, #14
    bne ov001_021fd1b8_L74
    bl native_fn_022040f8
    b ov001_021fd1b8_L84
ov001_021fd1b8_L74:
    bl native_fn_022040f8
    bl native_fn_0220412c
    bl native_fn_02204168
    bl native_fn_021fd178
ov001_021fd1b8_L84:
    ldr r0, =0x02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    bl native_fn_02202230
    cmp r5, #2
    bne ov001_021fd1b8_La8
    bl ov001_021fd1b8_L0
    mov r4, r0
    b ov001_021fd1b8_Lbc
ov001_021fd1b8_La8:
    cmp r5, #3
    moveq r4, #2
    beq ov001_021fd1b8_Lbc
    bl native_fn_020851d4
    bl native_fn_02085200
ov001_021fd1b8_Lbc:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
