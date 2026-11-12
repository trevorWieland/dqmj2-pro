/* ov001 row 0x021db1e8: 260 bytes.
 *
 * What it does: 65 instructions; 12 call(s) to 0x021db8d0, 0x021d8dec, 0x021db280, +9 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 12 calls (65 instructions, 12 calls, 6 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0xec
 *   branch +0x38 -> +0x98
 *   branch +0x44 -> +0x98
 *   branch +0x58 -> +0x98
 *   branch +0x6c -> +0x7c
 *   branch +0x88 -> +0x98
 *   branch +0x9c -> +0xe0
 *   branch +0xac -> +0xe0
 *   back edge +0xe8 -> +0x20
 *   back edge +0xf8 -> +0x0c
 *   test +0x14 cmp r0, #0
 *   test +0x34 cmp r2, #0
 *   test +0x40 cmp r0, #4
 *   test +0x54 cmp r0, #0
 *   test +0x68 cmp r5, #54
 *   test +0x7c cmp r5, #59
 *   test +0x84 cmpeq r0, #0
 *   test +0x98 cmp r5, #54
 *   test +0xa8 cmp r2, #0
 *   test +0xe4 cmp r5, #60
 *   test +0xf0 cmp r4, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021db1e8; the literal pool and
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
extern void native_fn_021dc940(void);
extern void native_fn_021dfcec(void);
extern void native_fn_021dfd30(void);
extern void native_fn_022094bc(void);
extern void native_fn_022047ec(void);
extern void native_fn_02204898(void);


asm u32 native_ov001_021db1e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    mov r4, #0
ov001_021db1e8_Lc:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021db1e8_Lec
    mov r5, #0
ov001_021db1e8_L20:
    mov r0, r5
    bl native_fn_021d8dec
    add r6, r7, r5
    add r1, r6, #512
    ldrsb r2, [r1, #104]
    cmp r2, #0
    ble ov001_021db1e8_L98
    ldrb r0, [r0, #0x2]
    cmp r0, #4
    bhi ov001_021db1e8_L98
    sub r0, r2, #1
    strb r0, [r6, #0x268]
    ldrsb r0, [r1, #104]
    cmp r0, #0
    bne ov001_021db1e8_L98
    mov r0, r7
    mov r1, r5
    bl native_fn_021dc940
    cmp r5, #54
    bne ov001_021db1e8_L7c
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    bl native_fn_021dfcec
ov001_021db1e8_L7c:
    cmp r5, #59
    ldreqb r0, [r7, #0x431]
    cmpeq r0, #0
    bne ov001_021db1e8_L98
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    bl native_fn_021dfd30
ov001_021db1e8_L98:
    cmp r5, #54
    bne ov001_021db1e8_Le0
    add r0, r6, #512
    ldrsb r2, [r0, #104]
    cmp r2, #0
    ble ov001_021db1e8_Le0
    ldrsb r1, [r0, #44]
    mov r0, r5
    bl native_fn_022094bc
    mov r6, r0
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    mov r2, r6
    bl native_fn_022047ec
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    mov r2, r6
    bl native_fn_02204898
ov001_021db1e8_Le0:
    add r5, r5, #1
    cmp r5, #60
    blt ov001_021db1e8_L20
ov001_021db1e8_Lec:
    add r4, r4, #1
    cmp r4, #3
    add r7, r7, #1088
    blt ov001_021db1e8_Lc
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
