/* ov001 row 0x021ef224: 372 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x168 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x16c -> constant 0x55555556 (image word 0x55555556)
 *   pool +0x170 -> constant 0x51eb851f (image word 0x51eb851f)
 *   branch +0x14 -> +0x3c
 *   branch +0x1c -> +0x30
 *   branch +0x20 -> +0x48
 *   branch +0x28 -> +0xf0
 *   branch +0x34 -> +0x140
 *   branch +0x40 -> +0xd4
 *   branch +0x50 -> +0x64
 *   branch +0xb0 -> +0xcc
 *   branch +0xf8 -> +0x10c
 *   test +0x0c cmp r2, #152
 *   test +0x18 cmp r2, #151
 *   test +0x24 cmp r2, #152
 *   test +0x30 cmp r2, #43
 *   test +0x3c cmp r2, #248
 *   test +0x4c cmp r0, #0
 *   test +0x58 cmp r0, #1
 *   test +0xac cmp r0, #0
 *   test +0xc0 cmp r0, #1
 *   test +0xf4 cmp r0, #0
 *   test +0x100 cmp r0, #1
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ef224; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020655d8(void);
extern void native_fn_021dbd24(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02026144(void);
extern void native_fn_02210ad0(void);
extern void ov001_record_field_1f2_021dbd30(void);
extern void native_fn_0203d294(void);
extern void native_fn_021dbcf0(void);


asm u32 native_ov001_021ef224 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    cmp r2, #152
    mov r0, #0
    bgt ov001_021ef224_L3c
    cmp r2, #151
    blt ov001_021ef224_L30
    beq ov001_021ef224_L48
    cmp r2, #152
    beq ov001_021ef224_Lf0
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_L30:
    cmp r2, #43
    beq ov001_021ef224_L140
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_L3c:
    cmp r2, #248
    beq ov001_021ef224_Ld4
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_L48:
    bl native_fn_020655d8
    cmp r0, #0
    beq ov001_021ef224_L64
    ldrb r0, [r5, #0x31e]
    cmp r0, #1
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
ov001_021ef224_L64:
    mov r0, r6
    bl native_fn_021dbd24
    ldr r1, [r5, #0x1e8]
    mov r4, r0
    ldrsh r0, [r1, #42]
    bl native_fn_02044cdc
    ldr r3, =0x88888889
    mov r1, r4, lsr #31
    smull r2, r12, r3, r4
    add r12, r4, r12
    add r12, r1, r12, asr #4
    mov r1, r0
    add r0, r12, #25
    bl native_fn_02026144
    mov r2, r0
    mov r0, r6
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_021ef224_Lcc
    mov r0, r5
    bl native_fn_021dbd24
    sub r0, r0, #1
    cmp r0, #1
    movlt r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_Lcc:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_Ld4:
    mov r0, r5
    bl ov001_record_field_1f2_021dbd30
    ldr r2, =0x55555556
    add r3, r0, #2
    smull r1, r0, r2, r3
    add r0, r0, r3, lsr #31
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_Lf0:
    bl native_fn_020655d8
    cmp r0, #0
    beq ov001_021ef224_L10c
    ldrb r0, [r5, #0x31e]
    cmp r0, #1
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, pc}
ov001_021ef224_L10c:
    mov r0, r5
    bl native_fn_021dbd24
    mov r4, r0
    mov r0, #31
    bl native_fn_0203d294
    add r0, r0, #30
    mul r1, r4, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #5
    add r0, r3, #1
    ldmia sp!, {r4, r5, r6, pc}
ov001_021ef224_L140:
    mov r0, r5
    bl native_fn_021dbcf0
    mov r4, r0
    mov r0, #6
    bl native_fn_0203d294
    mov r1, r4, asr #1
    add r1, r4, r1, lsr #30
    add r0, r0, r1, asr #2
    add r0, r0, #5
    ldmia sp!, {r4, r5, r6, pc}
}
