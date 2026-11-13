/* ov001 row 0x0220459c: 240 bytes.
 *
 * What it does: 60 instructions; 7 call(s) to 0x02204270, 0x02204250, 0x02204244, +4 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 7 calls (60 instructions, 7 calls, 2 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x94 -> +0xb0
 *   branch +0xac -> +0xcc
 *   test +0x14 cmp r5, #127
 *   test +0x40 tst r7, #1
 *   test +0x4c tst r7, #32
 *   test +0x90 cmp r0, #0
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220459c; the literal pool and
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

extern void native_fn_02204270(void);
extern void native_fn_02204250(void);
extern void native_fn_02204244(void);
extern void native_fn_022042ac(void);
extern void ov001_mode_byte_021db530(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);


asm u32 native_ov001_0220459c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, r0
    mov r7, r1
    bl native_fn_02204270
    mov r5, r0
    cmp r5, #127
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    bl native_fn_02204250
    mov r4, r0
    bl native_fn_02204244
    mov r1, #20
    mov r0, r5
    strb r1, [r4, #0x22]
    bl native_fn_022042ac
    mov r0, #0
    str r0, [r4]
    tst r7, #1
    moveq r0, #1
    str r0, [r4, #0x2c]
    tst r7, #32
    movne r0, #1
    str r6, [r4, #0x30]
    moveq r0, #0
    str r0, [r4, #0x34]
    mov r0, #0
    str r0, [r4, #0x38]
    str r7, [r4, #0x44]
    bl ov001_mode_byte_021db530
    mov r0, #0
    bl native_fn_02202384
    strh r0, [r4, #20]
    mov r1, r6
    mov r0, #0
    bl native_fn_02202398
    strh r0, [r4, #22]
    ldr r0, [r4, #0x2c]
    cmp r0, #0
    bne ov001_0220459c_Lb0
    ldrsh r0, [r4, #20]
    sub r0, r0, #16
    strh r0, [r4, #20]
    ldrsh r0, [r4, #22]
    add r0, r0, #4
    b ov001_0220459c_Lcc
ov001_0220459c_Lb0:
    ldrsh r1, [r4, #20]
    mov r0, r6, lsl #3
    add r0, r0, #4
    add r1, r1, #42
    strh r1, [r4, #20]
    ldrsh r1, [r4, #22]
    add r0, r1, r0
ov001_0220459c_Lcc:
    strh r0, [r4, #22]
    mov r0, #7
    strb r0, [r4, #0x20]
    mov r0, #3
    strb r0, [r4, #0x21]
    mov r1, #0
    mov r0, r5
    strb r1, [r4, #0x24]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
