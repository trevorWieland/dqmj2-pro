/* ov001 row 0x021f5ac4: 372 bytes.
 *
 * What it does: 91 instructions; 14 call(s) to 0x021dc4cc, 0x021dbcbc, 0x0207afec, +11 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 14 calls (91 instructions, 14 calls, 5 branches, 11 back edges, 2 literal slots).
 *
 *   pool +0x16c -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x170 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x2c -> +0x164
 *   branch +0x50 -> +0x130
 *   branch +0x7c -> +0x104
 *   branch +0x94 -> +0x104
 *   branch +0x9c -> +0xc4
 *   branch +0xc0 -> +0x104
 *   branch +0xcc -> +0x104
 *   test +0x28 cmp r0, #0
 *   test +0x48 cmp r6, #0
 *   test +0x74 cmp r7, #0
 *   test +0x78 cmpne r8, r7
 *   test +0x8c cmp r6, r7
 *   test +0x98 cmp r6, r8
 *   test +0xc4 cmp r7, r8
 *   test +0x130 cmp r10, #1
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f5ac4; the literal pool and
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

extern void native_fn_021dc4cc(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_0207afec(void);
extern void native_fn_021dbe68(void);
extern void native_fn_0203d294(void);
extern void native_fn_02026144(void);
extern void native_fn_0207d198(void);
extern void native_fn_021efbf4(void);
extern void native_fn_021db788(void);
extern void native_fn_022024d4(void);


asm u32 native_ov001_021f5ac4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r4, r1
    mov r5, r0
    mov r9, #0
    mov r7, r2
    mov r0, r4
    mov r2, r9
    mov r1, #1
    mov r6, r3
    bl native_fn_021dc4cc
    cmp r0, #0
    beq ov001_021f5ac4_L164
    mov r0, r4
    bl native_fn_021dbcbc
    mul r1, r7, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r10, r2, r1
    cmp r6, #0
    add r10, r0, r10, asr #5
    beq ov001_021f5ac4_L130
    ldr r0, =0x0223989c
    ldrh r0, [r0, #80]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    ldrsh r7, [r0, #24]
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldrsh r8, [r0, #26]
    cmp r7, #0
    cmpne r8, r7
    beq ov001_021f5ac4_L104
    mov r0, r5
    bl native_fn_021dbe68
    mov r6, r0
    cmp r6, r7
    movle r10, #1
    ble ov001_021f5ac4_L104
    cmp r6, r8
    blt ov001_021f5ac4_Lc4
    mov r0, #11
    bl native_fn_0203d294
    add r0, r0, #95
    mul r1, r10, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r10, r2, r1
    add r10, r0, r10, asr #5
    b ov001_021f5ac4_L104
ov001_021f5ac4_Lc4:
    cmp r7, r8
    moveq r10, #1
    beq ov001_021f5ac4_L104
    mov r0, #11
    bl native_fn_0203d294
    sub r1, r6, r7
    mov r6, r0
    mul r0, r10, r1
    sub r1, r8, r7
    bl native_fn_02026144
    add r1, r6, #95
    mul r1, r0, r1
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r10, r2, r1
    add r10, r0, r10, asr #5
ov001_021f5ac4_L104:
    ldr r0, =0x0223989c
    ldr r3, [r5, #0x1e8]
    ldrh r1, [r0, #80]
    mov r2, r10
    add r0, r3, #70
    bl native_fn_0207d198
    ldr r1, =0x0223989c
    mov r2, r5
    ldrh r1, [r1, #80]
    bl native_fn_021efbf4
    mov r10, r0
ov001_021f5ac4_L130:
    cmp r10, #1
    movgt r1, r10
    movle r1, #1
    mov r0, r4
    bl native_fn_021db788
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    rsb r2, r10, #0
    bl native_fn_022024d4
    add r0, r4, #768
    mov r1, #0
    strh r1, [r0, #32]
    add r9, r9, #1
ov001_021f5ac4_L164:
    mov r0, r9
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
