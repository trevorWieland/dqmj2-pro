/* ov001 row 0x0222186c: 176 bytes.
 *
 * What it does: 44 instructions; 8 call(s) to 0x021db8d0, 0x02218430, 0x02221900, +5 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 8 calls (44 instructions, 8 calls, 1 branch, 7 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x94
 *   branch +0x48 -> +0x94
 *   back edge +0x90 -> +0x4c
 *   back edge +0xa0 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x44 cmp r8, #0
 *   test +0x78 cmp r0, #0
 *   test +0x8c cmp r7, r8
 *   test +0x98 cmp r6, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222186c; the literal pool and
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
extern void native_fn_02218430(void);
extern void native_fn_0207afec(void);
extern void native_fn_0220e3a8(void);


asm u32 native_ov001_0222186c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #204
    ldr r10, [r0, #0x8]
    mov r6, #0
    add r5, sp, #4
    mov r4, #1
    mov r11, #200
ov001_0222186c_L1c:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0222186c_L94
    mov r0, r10
    mov r1, r5
    mov r2, r11
    bl native_fn_02218430
    mov r8, r0
    mov r7, #0
    cmp r8, #0
    ble ov001_0222186c_L94
ov001_0222186c_L4c:
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_0207afec
    ldrb r9, [r0, #0x1f]
    ldr r0, [r5, r7, lsl #2]
    bl native_fn_0207afec
    ldrb r2, [r0, #0x20]
    mov r1, r9
    mov r0, r10
    mov r3, r4
    str r4, [sp]
    bl native_fn_0220e3a8
    cmp r0, #0
    addeq sp, sp, #204
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r7, r7, #1
    cmp r7, r8
    blt ov001_0222186c_L4c
ov001_0222186c_L94:
    add r6, r6, #1
    cmp r6, #3
    add r10, r10, #1088
    blt ov001_0222186c_L1c
    mov r0, #0
    add sp, sp, #204
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
