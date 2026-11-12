/* ov001 row 0x022237d0: 188 bytes.
 *
 * What it does: 46 instructions; 8 call(s) to 0x021db8d0, 0x021dbd24, 0x021dbcbc, +5 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (46 instructions, 8 calls, 2 branches, 7 back edges, 1 literal slot).
 *
 *   pool +0xb8 -> constant 0x00002717 (image word 0x00002717)
 *   branch +0x2c -> +0x9c
 *   branch +0x50 -> +0x9c
 *   branch +0x70 -> +0x9c
 *   back edge +0x98 -> +0x74
 *   back edge +0xa8 -> +0x20
 *   test +0x28 cmp r0, #0
 *   test +0x4c cmp r8, r0, asr #2
 *   test +0x6c cmp r9, #0
 *   test +0x80 cmp r0, r4
 *   test +0x94 cmp r8, r9
 *   test +0xa0 cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022237d0; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_02218430(void);
extern void native_fn_0207afec(void);


asm u32 native_ov001_022237d0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #200
    mov r7, #0
    ldr r10, [r0, #0x8]
    ldr r4, =0x00002717
    add r6, sp, #0
    mov r5, #200
    mov r11, r7
ov001_022237d0_L20:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022237d0_L9c
    mov r0, r10
    bl native_fn_021dbd24
    mov r8, r0
    mov r0, r10
    bl native_fn_021dbcbc
    mov r1, r0, asr #1
    add r0, r0, r1, lsr #30
    cmp r8, r0, asr #2
    bgt ov001_022237d0_L9c
    mov r0, r10
    mov r1, r6
    mov r2, r5
    bl native_fn_02218430
    mov r9, r0
    mov r8, r11
    cmp r9, #0
    ble ov001_022237d0_L9c
ov001_022237d0_L74:
    ldr r0, [r6, r8, lsl #2]
    bl native_fn_0207afec
    ldrsh r0, [r0, #18]
    cmp r0, r4
    addeq sp, sp, #200
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r8, r8, #1
    cmp r8, r9
    blt ov001_022237d0_L74
ov001_022237d0_L9c:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_022237d0_L20
    mov r0, #0
    add sp, sp, #200
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
