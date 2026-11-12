/* ov001 row 0x021d73e4: 292 bytes.
 *
 * What it does: 70 instructions; 5 call(s) to 0x021d74f0, 0x020446f8, 0x020283dc, +2 more; loops (back edge at +0x88); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block load (70 instructions, 6 calls, 7 branches, 3 back edges, 3 literal slots).
 *
 *   pool +0x118 -> constant 0x0222fd50 (image word 0x0222fd50)
 *   pool +0x11c -> constant 0x0222fda0 (image word 0x0222fda0)
 *   pool +0x120 -> constant 0x02230d50 (image word 0x02230d50)
 *   branch +0x10 -> +0x110
 *   branch +0x1c -> +0x10c
 *   branch +0x38 -> +0x10c
 *   branch +0x4c -> +0x94
 *   branch +0x54 -> +0x78
 *   branch +0x60 -> +0x6c
 *   branch +0x74 -> +0x94
 *   branch +0x7c -> +0x94
 *   test +0x0c cmp r1, #0
 *   test +0x18 cmp r1, #0
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x50 cmp r0, #1
 *   test +0x5c cmp r1, #0
 *   test +0x78 cmp r0, #2
 *   1 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d73e4; the literal pool and
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

extern void native_fn_020446f8(void);
extern void native_fn_020283dc(void);
extern void native_fn_020283fc(void);
extern void native_fn_021d78dc(void);


asm u32 native_ov001_021d73e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r0, =0x0222fd50
    ldrb r1, [r0, #0x4e]
    cmp r1, #0
    bne ov001_021d73e4_L110
    ldrsh r1, [r0, #76]
    cmp r1, #0
    blt ov001_021d73e4_L10c
    mov r0, #120
    smulbb r1, r1, r0
    ldr r2, =0x0222fda0
    ldrb r0, [r2, r1]
    add r5, r2, r1
    cmp r0, #0
    beq ov001_021d73e4_L10c
    ldrb r0, [r5, #0x1]
    cmp r0, #0
    addeq r3, r5, #4
    addeq r4, r5, #16
    beq ov001_021d73e4_L94
    cmp r0, #1
    bne ov001_021d73e4_L78
    ldr r1, [r5, #0x1c]
    cmp r1, #0
    beq ov001_021d73e4_L6c
    add r0, r5, #28
    blx r1
ov001_021d73e4_L6c:
    add r3, r5, #96
    add r4, r5, #108
    b ov001_021d73e4_L94
ov001_021d73e4_L78:
    cmp r0, #2
    bne ov001_021d73e4_L94
    add r0, r5, #28
    mov r1, #0
    bl native_fn_020446f8
    add r3, r5, #36
    add r4, r5, #48
ov001_021d73e4_L94:
    ldr r0, =0x02230d50
    ldmia r3, {r10, lr}
    ldr r1, [r0, #0x748]
    ldr r2, [r0, #0x74c]
    ldr r12, [r3, #0x8]
    ldr r3, [r0, #0x750]
    ldr r9, [r4]
    ldr r8, [r0, #0x754]
    ldr r7, [r4, #0x4]
    ldr r5, [r4, #0x8]
    ldr r6, [r0, #0x758]
    ldr r4, [r0, #0x75c]
    add r1, r10, r1
    add r2, lr, r2
    add r3, r12, r3
    mov r0, #0
    bl native_fn_020283dc
    add r1, r9, r8
    add r2, r7, r6
    add r3, r5, r4
    mov r0, #0
    bl native_fn_020283fc
    ldr r0, =0x02230d50
    mov r1, #0
    str r1, [r0, #0x748]
    str r1, [r0, #0x74c]
    str r1, [r0, #0x750]
    str r1, [r0, #0x754]
    str r1, [r0, #0x758]
    str r1, [r0, #0x75c]
ov001_021d73e4_L10c:
    bl native_fn_021d78dc
ov001_021d73e4_L110:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
