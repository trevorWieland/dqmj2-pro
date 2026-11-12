/* ov001 row 0x02206aec: 420 bytes.
 *
 * What it does: 105 instructions; 15 call(s) to 0x022068a0, 0x02041814, 0x021fee40, +12 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 15 calls (105 instructions, 15 calls, 13 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x178
 *   branch +0x2c -> +0x44
 *   branch +0x30 -> +0x98
 *   branch +0x34 -> +0xa0
 *   branch +0x38 -> +0xa8
 *   branch +0x3c -> +0xe4
 *   branch +0x40 -> +0x138
 *   branch +0x4c -> +0x178
 *   branch +0x5c -> +0x90
 *   back edge +0x8c -> +0x68
 *   branch +0xb4 -> +0xd0
 *   back edge +0xcc -> +0xb8
 *   branch +0xe0 -> +0x178
 *   branch +0xec -> +0x124
 *   branch +0x100 -> +0x114
 *   back edge +0x120 -> +0xf4
 *   branch +0x134 -> +0x178
 *   branch +0x144 -> +0x16c
 *   back edge +0x168 -> +0x14c
 *   branch +0x180 -> +0x19c
 *   test +0x20 cmp r0, #5
 *   test +0x48 cmp r0, #1
 *   test +0x58 cmp r0, #0
 *   test +0x88 cmp r1, r0, asr #24
 *   test +0xb0 cmp r0, #0
 *   test +0xc8 cmp r5, r0
 *   test +0xe8 cmp r0, #0
 *   test +0xfc cmp r0, #0
 *   test +0x11c cmp r5, r0
 *   test +0x128 cmp r0, #0
 *   test +0x140 cmp r0, #0
 *   test +0x154 cmp r0, #7
 *   test +0x164 cmp r5, r0
 *   test +0x16c cmp r7, #0
 *   test +0x17c cmp r0, #2
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02206aec; the literal pool and
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

extern void native_fn_022068a0(void);
extern void native_fn_02041814(void);
extern void native_fn_021fee40(void);
extern void native_fn_0220727c(void);
extern void native_fn_02206c90(void);
extern void native_fn_022139f8(void);
extern void native_fn_02041538(void);


asm u32 native_ov001_02206aec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_022068a0
    add r1, sp, #0
    mov r5, #0
    mov r4, r0
    strh r5, [r1]
    strh r5, [r1, #2]
    ldr r0, [r4, #0x78]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b ov001_02206aec_L178
    b ov001_02206aec_L44
    b ov001_02206aec_L98
    b ov001_02206aec_La0
    b ov001_02206aec_La8
    b ov001_02206aec_Le4
    b ov001_02206aec_L138
ov001_02206aec_L44:
    bl native_fn_02041814
    cmp r0, #1
    beq ov001_02206aec_L178
    bl native_fn_021fee40
    ldr r0, [r4, #0x80]
    cmp r0, #0
    ble ov001_02206aec_L90
    mov r3, #1
    mov r2, r5
ov001_02206aec_L68:
    add r0, r4, r5, lsl #5
    str r3, [r0, #0x2c]
    strb r2, [r0, #0x32]
    strb r2, [r0, #0x33]
    add r0, r5, #1
    mov r0, r0, lsl #24
    ldr r1, [r4, #0x80]
    mov r5, r0, asr #24
    cmp r1, r0, asr #24
    bgt ov001_02206aec_L68
ov001_02206aec_L90:
    mov r0, #1
    str r0, [r4, #0x78]
ov001_02206aec_L98:
    mov r0, #2
    str r0, [r4, #0x78]
ov001_02206aec_La0:
    mov r0, #3
    str r0, [r4, #0x78]
ov001_02206aec_La8:
    ldr r0, [r4, #0x80]
    mov r5, #0
    cmp r0, #0
    ble ov001_02206aec_Ld0
ov001_02206aec_Lb8:
    mov r0, r5
    bl native_fn_0220727c
    ldr r0, [r4, #0x80]
    add r5, r5, #1
    cmp r5, r0
    blt ov001_02206aec_Lb8
ov001_02206aec_Ld0:
    mov r0, #0
    strb r0, [r4, #0x90]
    mov r0, #4
    str r0, [r4, #0x78]
    b ov001_02206aec_L178
ov001_02206aec_Le4:
    ldr r0, [r4, #0x80]
    cmp r0, #0
    ble ov001_02206aec_L124
    mov r6, r5
ov001_02206aec_Lf4:
    add r0, r4, r5, lsl #5
    ldrsb r0, [r0, #51]
    cmp r0, #0
    beq ov001_02206aec_L114
    mov r0, r5
    bl native_fn_0220727c
    add r0, r4, r5, lsl #5
    strb r6, [r0, #0x33]
ov001_02206aec_L114:
    ldr r0, [r4, #0x80]
    add r5, r5, #1
    cmp r5, r0
    blt ov001_02206aec_Lf4
ov001_02206aec_L124:
    ldrsb r0, [r4, #144]
    cmp r0, #0
    movne r0, #5
    strne r0, [r4, #0x78]
    b ov001_02206aec_L178
ov001_02206aec_L138:
    ldr r0, [r4, #0x80]
    mov r7, #1
    cmp r0, #0
    ble ov001_02206aec_L16c
    mov r6, r5
ov001_02206aec_L14c:
    mov r0, r5
    bl native_fn_02206c90
    cmp r0, #7
    ldr r0, [r4, #0x80]
    add r5, r5, #1
    movne r7, r6
    cmp r5, r0
    blt ov001_02206aec_L14c
ov001_02206aec_L16c:
    cmp r7, #0
    movne r0, #0
    strne r0, [r4, #0x10]
ov001_02206aec_L178:
    bl native_fn_022139f8
    cmp r0, #2
    bne ov001_02206aec_L19c
    mov r0, #1
    mov r1, #2
    mov r2, #30
    bl native_fn_02041538
    mov r0, #4
    str r0, [r4, #0x74]
ov001_02206aec_L19c:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
