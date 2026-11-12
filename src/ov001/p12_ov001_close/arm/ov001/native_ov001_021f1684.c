/* ov001 row 0x021f1684: 276 bytes.
 *
 * What it does: 67 instructions; 13 call(s) to 0x021f1710, 0x021f19f0, 0x0204a0b0, +10 more; loops (back edge at +0x54); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (67 instructions, 13 calls, 3 branches, 11 back edges, 2 literal slots).
 *
 *   pool +0x10c -> constant 0x02238f58 (image word 0x02238f58)
 *   pool +0x110 -> constant 0x02238f7c (image word 0x02238f7c)
 *   branch +0x14 -> +0x8c
 *   branch +0x40 -> +0x74
 *   back edge +0x88 -> +0x24
 *   branch +0xac -> +0xe4
 *   test +0x10 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x3c cmpne r1, #0
 *   test +0x84 cmp r1, r0, asr #24
 *   test +0x9c cmp r0, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xb8 cmp r0, #99
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1684; the literal pool and
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

extern void native_fn_021f19f0(void);
extern void native_fn_0204a0b0(void);
extern void native_fn_02085270(void);
extern void native_fn_02085418(void);
extern void native_fn_021e2bbc(void);
extern void native_fn_02044414(void);
extern void native_fn_02048094(void);
extern void native_fn_0204a04c(void);
extern void native_fn_021e2bd8(void);


asm u32 native_ov001_021f1684 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r8, =0x02238f58
    mov r7, #0
    ldr r0, [r8, #0x24]
    cmp r0, #0
    ble ov001_021f1684_L8c
    ldr r6, =0x02238f7c
    mov r5, r7
    mov r4, #3
ov001_021f1684_L24:
    add r0, r7, #3
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021f19f0
    cmp r0, #0
    ldrne r1, [r0]
    cmpne r1, #0
    beq ov001_021f1684_L74
    add r0, r6, r7, lsl #3
    ldr r9, [r1, #0x4]
    ldr r1, [r0, #0x8]
    mov r0, r9
    bl native_fn_0204a0b0
    mov r1, r5
    mov r2, r5
    add r0, r9, #60
    bl native_fn_02085270
    mov r0, r9
    mov r1, r4
    bl native_fn_02085418
ov001_021f1684_L74:
    add r0, r7, #1
    mov r0, r0, lsl #24
    ldr r1, [r8, #0x24]
    mov r7, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov001_021f1684_L24
ov001_021f1684_L8c:
    mov r0, #0
    bl native_fn_021f19f0
    mov r4, r0
    ldr r0, [r4]
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    bl native_fn_021e2bbc
    cmp r0, #0
    bne ov001_021f1684_Le4
    bl native_fn_02044414
    add r0, r0, #1
    cmp r0, #99
    movgt r0, #99
    mov r1, #0
    bl native_fn_02048094
    ldr r0, [r4]
    mov r1, #1
    ldr r0, [r0, #0x4]
    mov r2, r1
    mov r3, #14
    bl native_fn_0204a04c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov001_021f1684_Le4:
    bl native_fn_021e2bd8
    mov r1, #0
    bl native_fn_02048094
    ldr r0, [r4]
    mov r1, #1
    ldr r0, [r0, #0x4]
    mov r2, r1
    mov r3, #10
    bl native_fn_0204a04c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
