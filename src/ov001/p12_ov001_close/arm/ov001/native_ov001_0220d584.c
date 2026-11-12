/* ov001 row 0x0220d584: 232 bytes.
 *
 * What it does: 58 instructions; 9 call(s) to 0x02065d88, 0x021dbcbc, 0x02065d88, +6 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 9 calls (58 instructions, 9 calls, 6 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x20 -> +0x30
 *   branch +0x28 -> +0x50
 *   branch +0x2c -> +0x70
 *   branch +0x4c -> +0x70
 *   branch +0x78 -> +0xe0
 *   branch +0x84 -> +0xc0
 *   branch +0xb0 -> +0xc0
 *   test +0x1c cmp r0, #1
 *   test +0x24 cmp r0, #2
 *   test +0x70 cmp r4, #0
 *   test +0x7c cmp r4, #255
 *   test +0xac cmp r0, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xd0 cmp r0, r5
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220d584; the literal pool and
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

extern void native_fn_02065d88(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_0203d294(void);
extern void native_fn_02044424(void);


asm u32 native_ov001_0220d584 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r8, r1
    mov r9, r0
    mov r0, r8
    mvn r4, #0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x28]
    cmp r0, #1
    beq ov001_0220d584_L30
    cmp r0, #2
    beq ov001_0220d584_L50
    b ov001_0220d584_L70
ov001_0220d584_L30:
    mov r0, r9
    bl native_fn_021dbcbc
    mov r5, r0
    mov r0, r8
    bl native_fn_02065d88
    add r6, r9, #496
    ldrb r4, [r0, #0x2a]
    b ov001_0220d584_L70
ov001_0220d584_L50:
    mov r0, r9
    bl native_fn_021dbcf0
    mov r5, r0
    mov r0, r8
    bl native_fn_02065d88
    add r1, r9, #242
    ldrb r4, [r0, #0x2a]
    add r6, r1, #256
ov001_0220d584_L70:
    cmp r4, #0
    ldrsh r7, [r6]
    blt ov001_0220d584_Le0
    cmp r4, #255
    moveq r4, r5
    beq ov001_0220d584_Lc0
    mov r0, r8
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2b]
    sub r0, r0, r4
    add r0, r0, #1
    bl native_fn_0203d294
    add r4, r4, r0
    mov r0, #2048
    bl native_fn_02044424
    cmp r0, #0
    beq ov001_0220d584_Lc0
    ldrb r0, [r9, #0x31e]
    cmp r0, #0
    moveq r4, r4, lsl #1
ov001_0220d584_Lc0:
    ldrsh r0, [r6]
    add r0, r0, r4
    strh r0, [r6]
    ldrsh r0, [r6]
    cmp r0, r5
    strgth r5, [r6]
    ldrsh r0, [r6]
    sub r4, r0, r7
ov001_0220d584_Le0:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
