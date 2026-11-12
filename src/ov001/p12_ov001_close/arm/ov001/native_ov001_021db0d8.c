/* ov001 row 0x021db0d8: 272 bytes.
 *
 * What it does: 68 instructions; 12 call(s) to 0x021db8d0, 0x021d8dec, 0x021db1d4, +9 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 12 calls (68 instructions, 12 calls, 9 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x14 -> +0x108
 *   branch +0x40 -> +0xfc
 *   branch +0x4c -> +0xfc
 *   branch +0x54 -> +0x6c
 *   branch +0x68 -> +0xfc
 *   branch +0x84 -> +0xfc
 *   branch +0x98 -> +0xa8
 *   branch +0xbc -> +0xfc
 *   branch +0xc4 -> +0xd4
 *   branch +0xd8 -> +0xe8
 *   branch +0xec -> +0xfc
 *   back edge +0x104 -> +0x24
 *   test +0x10 cmp r0, #0
 *   test +0x3c cmp r1, #0
 *   test +0x48 cmp r0, #5
 *   test +0x50 cmp r9, #0
 *   test +0x64 tst r0, #128
 *   test +0x80 cmp r1, #0
 *   test +0x8c cmp r1, #0
 *   test +0x94 cmpne r0, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xc0 cmp r6, #36
 *   test +0xd4 cmp r6, #35
 *   test +0xe8 cmp r6, #54
 *   test +0x100 cmp r6, #60
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021db0d8; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021d8dec(void);
extern void native_fn_021dcec4(void);
extern void native_fn_021dc940(void);
extern void native_fn_021e2b0c(void);
extern void native_fn_021e2984(void);
extern void native_fn_021dfcec(void);


asm u32 native_ov001_021db0d8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r10, r0
    mov r9, r1
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021db0d8_L108
    mov r6, #0
    mov r5, #214
    mov r4, #215
ov001_021db0d8_L24:
    mov r0, r6
    bl native_fn_021d8dec
    add r8, r10, r6
    add r1, r8, #512
    ldrsb r1, [r1, #104]
    mov r7, r0
    cmp r1, #0
    ble ov001_021db0d8_Lfc
    ldrb r0, [r7, #0x2]
    cmp r0, #5
    blo ov001_021db0d8_Lfc
    cmp r9, #0
    bne ov001_021db0d8_L6c
    mov r0, r6
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r0, #128
    beq ov001_021db0d8_Lfc
ov001_021db0d8_L6c:
    add r0, r8, #512
    ldrsb r1, [r0, #104]
    sub r1, r1, #1
    strb r1, [r8, #0x268]
    ldrsb r1, [r0, #104]
    cmp r1, #0
    bne ov001_021db0d8_Lfc
    ldrb r1, [r7, #0x9]
    cmp r1, #0
    ldrnesb r0, [r0, #44]
    cmpne r0, #0
    beq ov001_021db0d8_La8
    mov r0, r10
    mov r1, r6
    bl native_fn_021dcec4
ov001_021db0d8_La8:
    mov r0, r10
    mov r1, r6
    bl native_fn_021dc940
    bl native_fn_021e2b0c
    cmp r0, #0
    bne ov001_021db0d8_Lfc
    cmp r6, #36
    bne ov001_021db0d8_Ld4
    mov r0, r10
    mov r1, r5
    bl native_fn_021e2984
ov001_021db0d8_Ld4:
    cmp r6, #35
    bne ov001_021db0d8_Le8
    mov r0, r10
    mov r1, r4
    bl native_fn_021e2984
ov001_021db0d8_Le8:
    cmp r6, #54
    bne ov001_021db0d8_Lfc
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    bl native_fn_021dfcec
ov001_021db0d8_Lfc:
    add r6, r6, #1
    cmp r6, #60
    blt ov001_021db0d8_L24
ov001_021db0d8_L108:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
