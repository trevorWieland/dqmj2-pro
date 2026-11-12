/* ov001 row 0x022092c0: 428 bytes.
 *
 * What it does: 107 instructions; 14 call(s) to 0x021d8dec, 0x021d8fa4, 0x022092ec, +11 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 14 calls (107 instructions, 14 calls, 13 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x1a4
 *   branch +0x3c -> +0x50
 *   back edge +0x58 -> +0x2c
 *   branch +0x64 -> +0x70
 *   branch +0x6c -> +0x80
 *   branch +0x7c -> +0x94
 *   branch +0x9c -> +0xac
 *   branch +0xbc -> +0xd0
 *   branch +0xd4 -> +0xf8
 *   branch +0xe4 -> +0x100
 *   branch +0xf4 -> +0x100
 *   branch +0x104 -> +0x1a4
 *   branch +0x10c -> +0x1a4
 *   branch +0x128 -> +0x14c
 *   branch +0x138 -> +0x14c
 *   branch +0x148 -> +0x198
 *   branch +0x15c -> +0x198
 *   branch +0x17c -> +0x198
 *   back edge +0x1a0 -> +0x118
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x54 cmp r7, #60
 *   test +0x5c cmp r4, #6
 *   test +0x68 cmp r10, #0
 *   test +0x80 cmp r1, r10
 *   test +0x98 cmp r0, r2
 *   test +0xa4 cmp r0, r2
 *   test +0xac cmp r2, r1
 *   test +0xb8 cmp r9, #0
 *   test +0xd0 cmp r9, #0
 *   test +0xe0 cmp r1, #0
 *   test +0xe8 cmp r1, r9
 *   test +0x100 cmp r6, #0
 *   test +0x108 cmp r10, #0
 *   test +0x124 cmp r0, #1
 *   test +0x134 cmp r0, r8
 *   test +0x158 cmp r0, #2
 *   test +0x168 cmp r0, r8
 *   test +0x170 cmpne r0, #0
 *   test +0x178 cmpne r0, #0
 *   test +0x19c cmp r7, #60
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022092c0; the literal pool and
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

extern void native_fn_021d8dec(void);
extern void native_fn_021d8fa4(void);
extern void native_fn_022091dc(void);
extern void native_fn_021d8eb4(void);
extern void native_fn_0220946c(void);


asm u32 native_ov001_022092c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r4, r1
    mov r5, r0
    mov r0, r4
    mov r10, r2
    mov r9, r3
    mov r6, #0
    bl native_fn_021d8dec
    movs r8, r0
    beq ov001_022092c0_L1a4
    mov r7, r6
ov001_022092c0_L2c:
    mov r0, r4
    mov r1, r7
    bl native_fn_021d8fa4
    cmp r0, #0
    bne ov001_022092c0_L50
    ldrsb r0, [r5, r7]
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_022092c0_L50:
    add r7, r7, #1
    cmp r7, #60
    blt ov001_022092c0_L2c
    cmp r4, #6
    ldrsb r1, [r5, r4]
    bne ov001_022092c0_L70
    cmp r10, #0
    bge ov001_022092c0_L80
ov001_022092c0_L70:
    add r0, r1, r10
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    b ov001_022092c0_L94
ov001_022092c0_L80:
    cmp r1, r10
    movgt r0, r1
    movle r0, r10
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
ov001_022092c0_L94:
    ldrsb r2, [r8]
    cmp r0, r2
    blt ov001_022092c0_Lac
    ldrsb r2, [r8, #1]
    cmp r0, r2
    movle r2, r0
ov001_022092c0_Lac:
    cmp r2, r1
    strneb r2, [r5, r4]
    movne r6, #1
    cmp r9, #0
    bne ov001_022092c0_Ld0
    ldr r1, [sp, #0x20]
    mov r0, r4
    bl native_fn_022091dc
    mov r9, r0
ov001_022092c0_Ld0:
    cmp r9, #0
    ble ov001_022092c0_Lf8
    add r0, r5, #60
    ldrsb r1, [r0, r4]
    cmp r1, #0
    blt ov001_022092c0_L100
    cmp r1, r9
    movle r1, r9
    strb r1, [r0, r4]
    b ov001_022092c0_L100
ov001_022092c0_Lf8:
    add r0, r5, r4
    strb r9, [r0, #0x3c]
ov001_022092c0_L100:
    cmp r6, #0
    beq ov001_022092c0_L1a4
    cmp r10, #0
    ble ov001_022092c0_L1a4
    mov r7, #0
    mvn r8, #1
ov001_022092c0_L118:
    mov r0, r4
    mov r1, r7
    bl native_fn_021d8eb4
    cmp r0, #1
    bne ov001_022092c0_L14c
    add r0, r5, r7
    ldrsb r0, [r0, #60]
    cmp r0, r8
    beq ov001_022092c0_L14c
    mov r0, r5
    mov r1, r7
    bl native_fn_0220946c
    b ov001_022092c0_L198
ov001_022092c0_L14c:
    mov r0, r4
    mov r1, r7
    bl native_fn_021d8eb4
    cmp r0, #2
    bne ov001_022092c0_L198
    add r1, r5, r7
    ldrsb r0, [r1, #60]
    cmp r0, r8
    ldrnesb r0, [r1]
    cmpne r0, #0
    ldrnesb r0, [r5, r4]
    cmpne r0, #0
    beq ov001_022092c0_L198
    mov r0, r5
    mov r1, r7
    bl native_fn_0220946c
    mov r0, r5
    mov r1, r4
    bl native_fn_0220946c
ov001_022092c0_L198:
    add r7, r7, #1
    cmp r7, #60
    blt ov001_022092c0_L118
ov001_022092c0_L1a4:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
