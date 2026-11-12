/* ov001 row 0x021f7908: 312 bytes.
 *
 * What it does: 77 instructions; 11 call(s) to 0x021db438, 0x021db438, 0x021db8d0, +8 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (77 instructions, 11 calls, 3 branches, 11 back edges, 1 literal slot).
 *
 *   pool +0x134 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x7c -> +0xc8
 *   branch +0x98 -> +0xbc
 *   branch +0xac -> +0xbc
 *   back edge +0xc4 -> +0x88
 *   back edge +0xd8 -> +0x70
 *   back edge +0xec -> +0x58
 *   test +0x14 cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x94 tst r0, #4
 *   test +0xa8 cmp r0, r4
 *   test +0xc0 cmp r7, #60
 *   test +0xcc cmp r6, #3
 *   test +0xe8 cmp r0, #2
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f7908; the literal pool and
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
extern void native_fn_021db8d0(void);
extern void native_fn_021d8dec(void);
extern void native_fn_021dc940(void);
extern void native_fn_021e29f8(void);
extern void native_fn_021e2a48(void);
extern void native_fn_021e048c(void);


asm u32 native_ov001_021f7908 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r2, #8
    movne r2, #16
    mov r0, #0
    and r2, r2, #255
    mov r1, r0
    str r2, [sp]
    bl native_fn_021db438
    str r0, [sp, #0x8]
    mov r0, #1
    mov r1, #0
    bl native_fn_021db438
    str r0, [sp, #0xc]
    mov r0, #0
    str r0, [sp, #0x4]
    mov r11, r0
    mvn r4, #1
ov001_021f7908_L58:
    ldr r0, [sp, #0x4]
    add r1, sp, #8
    ldr r10, [r1, r0, lsl #2]
    mov r6, #0
    mov r8, r10
    mov r9, r6
ov001_021f7908_L70:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f7908_Lc8
    mov r7, r11
    add r5, r10, r9
ov001_021f7908_L88:
    mov r0, r7
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r0, #4
    beq ov001_021f7908_Lbc
    add r0, r5, r7
    add r0, r0, #512
    ldrsb r0, [r0, #104]
    cmp r0, r4
    beq ov001_021f7908_Lbc
    mov r0, r5
    mov r1, r7
    bl native_fn_021dc940
ov001_021f7908_Lbc:
    add r7, r7, #1
    cmp r7, #60
    blt ov001_021f7908_L88
ov001_021f7908_Lc8:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    add r9, r9, #1088
    blt ov001_021f7908_L70
    ldr r0, [sp, #0x4]
    add r0, r0, #1
    str r0, [sp, #0x4]
    cmp r0, #2
    blt ov001_021f7908_L58
    ldr r1, =0x0223989c
    mov r0, #1
    ldr r1, [r1, #0x84]
    ldrb r1, [r1, #0x31e]
    bl native_fn_021e29f8
    ldr r0, [sp]
    orr r0, r0, #1
    mvn r0, r0
    and r0, r0, #255
    bl native_fn_021e2a48
    bl native_fn_021e048c
    ldr r0, =0x0223989c
    mov r1, #27
    strb r1, [r0, #0x1b]
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
