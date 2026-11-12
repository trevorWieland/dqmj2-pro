/* ov001 row 0x021fc63c: 252 bytes.
 *
 * What it does: 62 instructions; 7 call(s) to 0x021db530, 0x021fc724, 0x021db438, +4 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (62 instructions, 7 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0xf8 -> constant 0x02239ca4 (image word 0x02239ca4)
 *   branch +0x20 -> +0xe8
 *   back edge +0xe4 -> +0x34
 *   test +0x18 cmp r7, #0
 *   test +0xdc cmp r7, r0, asr #24
 *   2 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fc63c; the literal pool and
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

extern void native_fn_021db530(void);
extern void native_fn_021db438(void);
extern void native_fn_0206d250(void);
extern void native_fn_021fe4ac(void);
extern void native_fn_022023c4(void);


asm u32 native_ov001_021fc63c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    mov r0, #0
    bl native_fn_021db530
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #0
    mov r6, #0
    ble ov001_021fc63c_Le8
    mov r5, #1
    ldr r10, =0x02239ca4
    mov r4, #8
    mov r11, r5
ov001_021fc63c_L34:
    mov r0, #0
    mov r1, r6
    bl native_fn_021db438
    ldrb r1, [r10, #0x4]
    ldrsb r0, [r10, #12]
    mov r1, r1, asr #3
    add r1, r1, #1
    and r8, r1, #255
    bl native_fn_0206d250
    add r2, r0, #1
    ldrb r3, [r10, #0x5]
    mov r0, #40
    add r1, r6, #16
    mla r0, r2, r0, r3
    and r0, r0, #255
    mov r0, r0, asr #3
    and r9, r0, #255
    mov r0, r1, lsl #24
    str r9, [sp]
    mov r1, #8
    stmib sp, {r1, r5}
    str r5, [sp, #0xc]
    mov r0, r0, asr #24
    mov r2, #127
    mov r3, r8
    str r5, [sp, #0x10]
    bl native_fn_021fe4ac
    add r0, r9, #1
    and r0, r0, #255
    stmia sp, {r0, r4, r11}
    add r0, r6, #19
    mov r0, r0, lsl #24
    str r11, [sp, #0xc]
    mov r3, r8
    mov r0, r0, asr #24
    mov r1, r4
    mov r2, #127
    str r11, [sp, #0x10]
    bl native_fn_021fe4ac
    add r0, r6, #1
    mov r0, r0, lsl #24
    add r10, r10, #16
    cmp r7, r0, asr #24
    mov r6, r0, asr #24
    bgt ov001_021fc63c_L34
ov001_021fc63c_Le8:
    mov r0, #1
    bl native_fn_022023c4
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
