/* ov001 row 0x021eb024: 288 bytes.
 *
 * What it does: 70 instructions; 7 call(s) to 0x0205d790, 0x021e9cd8, 0x02041f74, +4 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (70 instructions, 7 calls, 7 branches, 7 back edges, 2 literal slots).
 *
 *   pool +0x118 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x11c -> constant 0x02238d7c (image word 0x02238d7c)
 *   branch +0x18 -> +0x10c
 *   branch +0x28 -> +0x90
 *   branch +0x30 -> +0x90
 *   branch +0x3c -> +0x50
 *   branch +0x4c -> +0x10c
 *   branch +0x8c -> +0x10c
 *   branch +0x94 -> +0xbc
 *   test +0x14 cmp r0, #0
 *   test +0x2c cmp r4, #0
 *   test +0x90 cmp r4, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xcc cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eb024; the literal pool and
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

extern void native_fn_0205d790(void);
extern void native_fn_021e9cd8(void);
extern void native_fn_02041f74(void);
extern void native_fn_021e9d20(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021d8b4c(void);


asm u32 native_ov001_021eb024 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #16
    mov r5, r0
    ldrsh r0, [r5, #12]
    mov r4, r1
    cmp r0, #0
    beq ov001_021eb024_L10c
    ldrh r1, [r5, #8]
    mov r1, r1, lsl #16
    movs r1, r1, lsr #28
    bne ov001_021eb024_L90
    cmp r4, #0
    beq ov001_021eb024_L90
    bl native_fn_0205d790
    movs r2, r0
    bmi ov001_021eb024_L50
    ldrsh r0, [r5, #12]
    mov r1, r4
    bl native_fn_021e9cd8
    b ov001_021eb024_L10c
ov001_021eb024_L50:
    add r1, sp, #4
    mov r0, r4
    bl native_fn_02041f74
    ldrb r0, [r4, #0x31e]
    ldr r2, =0x66666667
    str r0, [sp]
    ldr r1, [sp, #0xc]
    ldrsh r0, [r5, #12]
    mov r4, r1, lsl #3
    smull r1, r3, r2, r4
    mov r4, r4, lsr #31
    ldr r1, [sp, #0x4]
    ldr r2, [sp, #0x8]
    add r3, r4, r3, asr #2
    bl native_fn_021e9d20
    b ov001_021eb024_L10c
ov001_021eb024_L90:
    cmp r4, #0
    bne ov001_021eb024_Lbc
    ldr r0, =0x02238d7c
    mov r1, #0
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    bl ov001_side_slot_record_021db438
    mov r4, r0
ov001_021eb024_Lbc:
    ldr r0, =0x02238d7c
    add r1, sp, #4
    ldr r0, [r0, #0x54]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #3
    movne r0, #11
    bl native_fn_021d8b4c
    ldrb r0, [r4, #0x31e]
    ldr r2, =0x66666667
    str r0, [sp]
    ldr r1, [sp, #0xc]
    ldrsh r0, [r5, #12]
    mov r4, r1, lsl #3
    smull r1, r3, r2, r4
    mov r4, r4, lsr #31
    ldr r1, [sp, #0x4]
    ldr r2, [sp, #0x8]
    add r3, r4, r3, asr #2
    bl native_fn_021e9d20
ov001_021eb024_L10c:
    mvn r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, pc}
}
