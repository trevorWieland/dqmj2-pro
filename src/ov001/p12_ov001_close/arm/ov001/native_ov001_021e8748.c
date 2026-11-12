/* ov001 row 0x021e8748: 336 bytes.
 *
 * What it does: 84 instructions; 12 call(s) to 0x021db578, 0x020443ec, 0x020443ec, +9 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 13 calls (84 instructions, 13 calls, 8 branches, 9 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x144
 *   branch +0x24 -> +0x40
 *   branch +0x30 -> +0x40
 *   branch +0x3c -> +0x144
 *   branch +0x4c -> +0x144
 *   branch +0xa4 -> +0x134
 *   branch +0xe0 -> +0x10c
 *   branch +0x108 -> +0x124
 *   back edge +0x130 -> +0xb8
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x2c cmp r0, #5
 *   test +0x38 cmp r0, #8
 *   test +0x48 cmp r0, #0
 *   test +0xa0 cmp r7, r1
 *   test +0xdc cmp r0, #0
 *   test +0xe8 cmp r1, r10
 *   test +0xfc cmp r0, #0
 *   test +0x110 cmp r0, r9
 *   test +0x12c cmp r7, r0
 *   test +0x134 cmp r8, #100
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e8748; the literal pool and
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

extern void native_fn_021db578(void);
extern void native_fn_020443ec(void);
extern void native_fn_02044424(void);
extern void native_fn_02218410(void);
extern void native_fn_021db438(void);
extern void native_fn_02218400(void);
extern void native_fn_02223f10(void);


asm u32 native_ov001_021e8748 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #36
    mov r0, #3
    mov r8, #0
    bl native_fn_021db578
    cmp r0, #0
    beq ov001_021e8748_L144
    bl native_fn_020443ec
    cmp r0, #0
    beq ov001_021e8748_L40
    bl native_fn_020443ec
    cmp r0, #5
    beq ov001_021e8748_L40
    bl native_fn_020443ec
    cmp r0, #8
    bne ov001_021e8748_L144
ov001_021e8748_L40:
    mov r0, #67108864
    bl native_fn_02044424
    cmp r0, #0
    bne ov001_021e8748_L144
    add r0, sp, #4
    add r1, sp, #0
    bl native_fn_02218410
    mov r0, #1
    mov r1, #0
    bl native_fn_021db438
    str r0, [sp, #0xc]
    mov r0, #0
    mov r1, r0
    bl native_fn_021db438
    mov r1, #0
    str r0, [sp, #0x10]
    mov r0, #1
    str r1, [sp, #0x14]
    str r1, [sp, #0x18]
    str r1, [sp, #0x1c]
    bl native_fn_021db438
    ldr r7, [sp, #0x4]
    ldr r1, [sp]
    str r0, [sp, #0x8]
    cmp r7, r1
    bgt ov001_021e8748_L134
    mvn r5, #0
    sub r10, r5, #127
    mov r9, r10
    add r4, sp, #8
ov001_021e8748_Lb8:
    mov r0, r7
    bl native_fn_02218400
    mov r6, r0
    str r5, [sp, #0x20]
    ldrh r0, [r6]
    bl native_fn_02223f10
    mov r1, r0
    mov r0, r4
    blx r1
    cmp r0, #0
    beq ov001_021e8748_L10c
    ldrsb r1, [r6, #2]
    cmp r1, r10
    addeq sp, sp, #36
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
    ldr r0, [sp, #0x20]
    cmp r0, #0
    addlt r8, r8, r1
    addge r8, r8, r0
    b ov001_021e8748_L124
ov001_021e8748_L10c:
    ldrsb r0, [r6, #3]
    cmp r0, r9
    addeq sp, sp, #36
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
    add r8, r8, r0
ov001_021e8748_L124:
    ldr r0, [sp]
    add r7, r7, #1
    cmp r7, r0
    ble ov001_021e8748_Lb8
ov001_021e8748_L134:
    cmp r8, #100
    addgt sp, sp, #36
    movgt r0, #1
    ldmgtia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
ov001_021e8748_L144:
    mov r0, #0
    add sp, sp, #36
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
