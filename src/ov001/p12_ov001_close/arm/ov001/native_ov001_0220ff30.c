/* ov001 row 0x0220ff30: 268 bytes.
 *
 * What it does: 67 instructions; 9 call(s) to 0x021db438, 0x021db8d0, 0x021d8dec, +6 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 9 calls (67 instructions, 9 calls, 9 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0xf4
 *   branch +0x44 -> +0xe8
 *   branch +0x60 -> +0xe8
 *   branch +0x68 -> +0x98
 *   branch +0x7c -> +0x90
 *   branch +0x8c -> +0xe8
 *   branch +0x9c -> +0xe0
 *   branch +0xb0 -> +0xd8
 *   branch +0xc4 -> +0xe8
 *   branch +0xd4 -> +0xe8
 *   back edge +0xf0 -> +0x34
 *   back edge +0x100 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x40 tst r10, r0
 *   test +0x54 cmp r1, #0
 *   test +0x5c cmpne r0, r4
 *   test +0x64 cmp r10, #1
 *   test +0x78 cmp r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0x98 cmp r10, #4
 *   test +0xac cmp r0, #0
 *   test +0xc0 cmp r0, #2
 *   test +0xd0 cmp r0, #0
 *   test +0xec cmp r7, #60
 *   test +0xf8 cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220ff30; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021d8dec(void);


asm u32 native_ov001_0220ff30 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r10, r1
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r6, #0
    mov r8, r0
    mov r5, r6
ov001_0220ff30_L1c:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0220ff30_Lf4
    mov r7, r5
    mvn r4, #1
ov001_0220ff30_L34:
    mov r0, r7
    bl native_fn_021d8dec
    ldrb r0, [r0, #0x3]
    tst r10, r0
    beq ov001_0220ff30_Le8
    add r9, r8, r7
    add r0, r9, #512
    ldrsb r1, [r0, #44]
    cmp r1, #0
    ldrnesb r0, [r0, #104]
    cmpne r0, r4
    beq ov001_0220ff30_Le8
    cmp r10, #1
    bne ov001_0220ff30_L98
    mov r0, r7
    bl native_fn_021d8dec
    ldrsb r0, [r0]
    cmp r0, #0
    bge ov001_0220ff30_L90
    add r0, r9, #512
    ldrsb r0, [r0, #44]
    cmp r0, #0
    bge ov001_0220ff30_Le8
ov001_0220ff30_L90:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_0220ff30_L98:
    cmp r10, #4
    bne ov001_0220ff30_Le0
    mov r0, r7
    bl native_fn_021d8dec
    ldrsb r0, [r0, #8]
    cmp r0, #0
    beq ov001_0220ff30_Ld8
    mov r0, r7
    bl native_fn_021d8dec
    ldrsb r0, [r0, #8]
    cmp r0, #2
    bne ov001_0220ff30_Le8
    add r0, r9, #512
    ldrsb r0, [r0, #44]
    cmp r0, #0
    ble ov001_0220ff30_Le8
ov001_0220ff30_Ld8:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_0220ff30_Le0:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_0220ff30_Le8:
    add r7, r7, #1
    cmp r7, #60
    blt ov001_0220ff30_L34
ov001_0220ff30_Lf4:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    blt ov001_0220ff30_L1c
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
