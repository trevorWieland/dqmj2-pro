/* ov001 row 0x02212b68: 488 bytes.
 *
 * What it does: 121 instructions; 15 call(s) to 0x022134a0, 0x0205f98c, 0x021f1ba0, +12 more; loops (back edge at +0x68); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (121 instructions, 15 calls, 10 branches, 16 back edges, 1 literal slot).
 *
 *   pool +0x1e4 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x28 -> +0x154
 *   branch +0x74 -> +0x90
 *   branch +0x7c -> +0x90
 *   branch +0x8c -> +0xc4
 *   back edge +0xdc -> +0x60
 *   back edge +0x178 -> +0x158
 *   test +0x24 cmp r7, #1000
 *   test +0x70 cmp r6, #26
 *   test +0x78 cmp r7, #0
 *   test +0xd4 cmp r6, #24
 *   test +0x174 cmp r4, #24
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02212b68; the literal pool and
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

extern void native_fn_022134a0(void);
extern void native_fn_0205f98c(void);
extern void native_fn_021f1ba0(void);
extern void native_fn_02048a60(void);


asm u32 native_ov001_02212b68 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r10, r0
    ldr r7, [r10, #0x30]
    ldr r4, =0x66666667
    mov r1, r7, lsr #31
    smull r3, r2, r4, r7
    add r2, r1, r2, asr #2
    mov r1, #100
    bl native_fn_022134a0
    cmp r7, #1000
    beq ov001_02212b68_L154
    mov r5, r4
    smull r1, r8, r5, r7
    mov r0, r7, lsr #31
    mov r2, #10
    add r8, r0, r8, asr #2
    smull r0, r1, r2, r8
    mov r3, r7
    sub r8, r7, r0
    smull r0, r7, r5, r3
    mov r0, r3, lsr #31
    add r7, r0, r7, asr #2
    mov r6, #26
    mov r4, r2
ov001_02212b68_L60:
    ldr r0, [r10, #0x1c]
    and r1, r6, #255
    bl native_fn_0205f98c
    mov r9, r0
    cmp r6, #26
    bge ov001_02212b68_L90
    cmp r7, #0
    bne ov001_02212b68_L90
    ldr r0, [r9, #0x7c]
    bic r0, r0, #2
    str r0, [r9, #0x7c]
    b ov001_02212b68_Lc4
ov001_02212b68_L90:
    mov r0, r7, lsr #31
    smull r1, r2, r5, r7
    add r2, r0, r2, asr #2
    smull r0, r1, r4, r2
    sub r2, r7, r0
    and r0, r2, #255
    add r1, r0, #168
    mov r0, r9
    and r1, r1, #255
    bl native_fn_021f1ba0
    ldr r0, [r9, #0x7c]
    orr r0, r0, #2
    str r0, [r9, #0x7c]
ov001_02212b68_Lc4:
    mov r1, r7
    smull r0, r7, r5, r1
    mov r0, r1, lsr #31
    sub r6, r6, #1
    cmp r6, #24
    add r7, r0, r7, asr #2
    bge ov001_02212b68_L60
    ldr r0, [r10, #0x1c]
    mov r1, #28
    bl native_fn_0205f98c
    mov r4, r0
    mov r1, #190
    bl native_fn_021f1ba0
    ldr r0, [r4, #0x7c]
    mov r1, #29
    orr r0, r0, #2
    str r0, [r4, #0x7c]
    ldr r0, [r10, #0x1c]
    bl native_fn_0205f98c
    add r1, r8, #180
    mov r4, r0
    and r1, r1, #255
    bl native_fn_021f1ba0
    ldr r0, [r4, #0x7c]
    mov r1, #27
    orr r0, r0, #2
    str r0, [r4, #0x7c]
    ldr r0, [r10, #0x1c]
    bl native_fn_0205f98c
    mov r4, r0
    mov r1, #178
    bl native_fn_021f1ba0
    ldr r0, [r4, #0x7c]
    orr r0, r0, #2
    str r0, [r4, #0x7c]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_02212b68_L154:
    mov r4, #26
ov001_02212b68_L158:
    ldr r0, [r10, #0x1c]
    and r1, r4, #255
    bl native_fn_0205f98c
    ldr r1, [r0, #0x7c]
    sub r4, r4, #1
    bic r1, r1, #2
    str r1, [r0, #0x7c]
    cmp r4, #24
    bge ov001_02212b68_L158
    ldr r0, [r10, #0x1c]
    mov r1, #28
    bl native_fn_0205f98c
    ldr r2, [r0, #0x7c]
    mov r1, #29
    bic r2, r2, #2
    str r2, [r0, #0x7c]
    ldr r0, [r10, #0x1c]
    bl native_fn_0205f98c
    ldr r2, [r0, #0x7c]
    mov r1, #27
    bic r2, r2, #2
    str r2, [r0, #0x7c]
    ldr r0, [r10, #0x1c]
    bl native_fn_0205f98c
    mov r4, r0
    mov r1, #179
    bl native_fn_021f1ba0
    ldr r1, [r4, #0x7c]
    mov r0, r4
    orr r1, r1, #2
    str r1, [r4, #0x7c]
    ldrsh r1, [r10, #20]
    ldrsh r2, [r10, #22]
    bl native_fn_02048a60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
