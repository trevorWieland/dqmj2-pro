/* ov001 row 0x021fc76c: 388 bytes.
 *
 * What it does: 96 instructions; 16 call(s) to 0x021db438, 0x02049ad0, 0x02049ffc, +13 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (96 instructions, 16 calls, 2 branches, 16 back edges, 1 literal slot).
 *
 *   pool +0x180 -> constant 0x021c96a0 (image word 0x021c96a0)
 *   branch +0x5c -> +0xac
 *   branch +0xa8 -> +0xcc
 *   back edge +0x174 -> +0x24
 *   test +0x24 cmp r10, #0
 *   test +0x58 cmp r10, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xd4 cmp r10, #0
 *   test +0x170 cmp r10, #2
 *   1 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fc76c; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_02085284(void);
extern void native_fn_021dbd24(void);
extern void native_fn_0207c164(void);
extern void native_fn_021dbd30(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02008be0(void);
extern void native_fn_02046af4(void);
extern void native_fn_02087a48(void);
extern void native_fn_020877bc(void);


asm u32 native_ov001_021fc76c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #136
    mov r11, r0
    mov r1, r11
    mov r0, #0
    bl native_fn_021db438
    mov r7, r0
    mov r10, #0
    add r4, sp, #8
ov001_021fc76c_L24:
    cmp r10, #0
    moveq r0, #16
    movne r0, #19
    add r0, r11, r0
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    mov r5, r0
    ldr r0, [r5]
    mov r9, #1
    ldr r6, [r0, #0x4]
    mov r0, r6
    bl native_fn_02049ffc
    cmp r10, #0
    bne ov001_021fc76c_Lac
    mov r0, r7
    bl native_fn_021dbcbc
    mov r0, r0, lsl #16
    mov r8, r0, asr #16
    add r0, r6, #60
    mov r1, #5
    mov r2, r9
    mov r3, #2
    bl native_fn_02085284
    mov r0, r7
    bl native_fn_021dbd24
    mov r1, r8
    mov r8, r0
    mov r0, r8, lsl #16
    mov r0, r0, asr #16
    bl native_fn_0207c164
    cmp r0, #0
    movne r9, #7
    b ov001_021fc76c_Lcc
ov001_021fc76c_Lac:
    add r0, r6, #60
    mov r1, #5
    mov r2, r9
    mov r3, #3
    bl native_fn_02085284
    mov r0, r7
    bl native_fn_021dbd30
    mov r8, r0
ov001_021fc76c_Lcc:
    mov r0, r5
    bl native_fn_02049f4c
    cmp r10, #0
    moveq r0, #1
    movne r0, #0
    mov r0, r0, lsl #16
    mov r5, r0, asr #16
    mov r0, #0
    mov r1, r4
    mov r2, #128
    bl native_fn_02008be0
    str r4, [sp]
    mov r0, #255
    str r0, [sp, #0x4]
    ldr r0, =0x021c96a0
    ldr r1, [r6, #0x68]
    mov r2, #31
    mov r3, #0
    bl native_fn_02046af4
    mov r0, #1
    stmia sp, {r0, r4}
    mov r0, r6
    mov r1, #1
    mov r2, #3
    mov r3, r5
    bl native_fn_02087a48
    mov r0, r8
    mov r1, r4
    mov r2, #128
    mov r3, #4
    bl native_fn_020877bc
    str r9, [sp]
    str r0, [sp, #0x4]
    mov r3, r5
    mov r0, r6
    mov r1, #1
    mov r2, #21
    bl native_fn_02087a48
    add r0, r10, #1
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    cmp r10, #2
    blt ov001_021fc76c_L24
    add sp, sp, #136
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
