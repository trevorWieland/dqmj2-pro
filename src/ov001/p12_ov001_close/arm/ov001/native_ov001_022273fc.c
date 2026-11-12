/* ov001 row 0x022273fc: 280 bytes.
 *
 * What it does: 69 instructions; 14 call(s) to 0x02223fe8, 0x02226bdc, 0x02224900, +11 more; loops (back edge at +0x28); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block copy loop (69 instructions, 14 calls, 2 branches, 13 back edges, 1 literal slot).
 *
 *   pool +0x114 -> native_data_0222e884 (image word 0x0222e884)
 *   branch +0xb4 -> +0xfc
 *   branch +0xd4 -> +0xf0
 *   branch +0xe0 -> +0xf0
 *   back edge +0xf8 -> +0xcc
 *   test +0xb0 cmp r0, #2
 *   test +0xd0 cmp r1, #0
 *   test +0xdc cmp r1, #0
 *   test +0xe8 cmp r1, #0
 *   test +0xf4 cmp r4, #3
 *   2 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022273fc; the literal pool and
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

extern u8 native_data_0222e884[];
extern void native_fn_02223fe8(void);
extern void native_fn_02226bdc(void);
extern void native_fn_02224900(void);
extern void native_fn_02225bac(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02225854(void);
extern void native_fn_02224804(void);
extern void native_fn_02223f20(void);
extern void native_fn_02224050(void);
extern void native_fn_02226cb0(void);


asm u32 native_ov001_022273fc (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #36
    ldr r1, =native_data_0222e884
    add r3, sp, #24
    mov r5, r0
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r4, [r5, #0x4]
    mov r0, r3
    mov r1, r4
    bl native_fn_02223fe8
    add r0, sp, #24
    mov r1, r5
    mov r2, #22
    bl native_fn_02226bdc
    add r0, sp, #24
    mov r1, r4
    bl native_fn_02224900
    add r0, sp, #24
    mov r1, r4
    mov r2, #55
    bl native_fn_02225bac
    add r0, sp, #24
    mov r1, r4
    mov r2, #54
    bl native_fn_02225bac
    add r0, sp, #24
    add r1, sp, #0
    mov r2, #12
    bl native_fn_02008e0c
    add r0, sp, #24
    mov r1, r4
    bl native_fn_02225854
    add r0, sp, #24
    add r1, sp, #12
    mov r2, #12
    bl native_fn_02008e0c
    mov r1, r4
    add r0, sp, #24
    mov r2, #0
    mov r3, #5
    bl native_fn_02224804
    add r0, sp, #24
    bl native_fn_02223f20
    cmp r0, #2
    blt ov001_022273fc_Lfc
    mov r4, #0
    mov r0, #1
    add r2, sp, #12
    add r3, sp, #0
    add r12, sp, #24
ov001_022273fc_Lcc:
    ldr r1, [r12, r4, lsl #2]
    cmp r1, #0
    bne ov001_022273fc_Lf0
    ldr r1, [r3, r4, lsl #2]
    cmp r1, #0
    beq ov001_022273fc_Lf0
    ldr r1, [r2, r4, lsl #2]
    cmp r1, #0
    streq r0, [r12, r4, lsl #2]
ov001_022273fc_Lf0:
    add r4, r4, #1
    cmp r4, #3
    blt ov001_022273fc_Lcc
ov001_022273fc_Lfc:
    add r0, sp, #24
    bl native_fn_02224050
    add r0, sp, #24
    bl native_fn_02226cb0
    add sp, sp, #36
    ldmia sp!, {r4, r5, pc}
}
