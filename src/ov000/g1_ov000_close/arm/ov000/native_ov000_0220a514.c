/* ov000 row 0x0220a514: 316 bytes.
 *
 * What it does: 77 instructions; 7 call(s) to 0x021d8a50, 0x0220a5d4, 0x0220a4e4, +4 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x134 -> constant 0x02238634 (image word 0x02238634)
 *   pool +0x138 -> constant 0x00bd1000 (image word 0x00bd1000)
 *   branch +0x30 -> +0x11c
 *   branch +0x48 -> +0x11c
 *   branch +0x5c -> +0x9c
 *   branch +0xac -> +0xc0
 *   branch +0xbc -> +0x11c
 *   branch +0xc8 -> +0x11c
 *   branch +0xd8 -> +0xfc
 *   branch +0xe8 -> +0xfc
 *   branch +0xf8 -> +0x11c
 *   back edge +0x128 -> +0x28
 *   test +0x2c cmp r0, #0
 *   test +0x44 cmp r0, #10
 *   test +0x50 cmp r0, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xc4 cmp r0, #2
 *   test +0xe4 cmp r0, #0
 *   test +0xf4 cmp r0, #0
 *   test +0x120 cmp r4, #48
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a514; the literal pool and
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

extern void native_fn_021d8a50(void);
extern void native_fn_0220a4e4(void);
extern void native_fn_021d8c18(void);


asm u32 native_ov000_0220a514 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r0, #0
    mov r4, r1
    bl native_fn_021d8a50
    mov r1, #20
    mla r9, r10, r1, r4
    ldr r8, =0x02238634
    mov r5, r0
    mov r4, #0
ov000_0220a514_L28:
    ldrb r0, [r8, #0x274]
    cmp r0, #0
    beq ov000_0220a514_L11c
    ldrb r11, [r8, #0x1e2]
    mov r0, #0
    strb r0, [r8, #0x1e2]
    ldrb r0, [r8, #0x278]
    cmp r0, #10
    bhs ov000_0220a514_L11c
    ldrb r0, [r8, #0x1e4]
    cmp r0, #0
    movne r7, #0
    movne r6, r7
    bne ov000_0220a514_L9c
    ldr r1, [r5, #0x4]
    ldr r0, [r8, #0x74]
    ldr r6, [r5]
    sub r2, r1, r0
    smull r1, r0, r2, r2
    ldr r2, [r8, #0x70]
    ldr r3, [r5, #0x8]
    sub r2, r6, r2
    smlal r1, r0, r2, r2
    ldr r2, [r8, #0x78]
    sub r2, r3, r2
    smlal r1, r0, r2, r2
    mov r7, r1, lsr #12
    mov r6, r0, asr #12
    orr r7, r7, r0, lsl #20
ov000_0220a514_L9c:
    ldr r0, =0x00bd1000
    subs r0, r7, r0
    mov r0, #0
    sbcs r0, r6, r0
    blt ov000_0220a514_Lc0
    mov r0, r4
    bl native_fn_0220a4e4
    cmp r0, #0
    beq ov000_0220a514_L11c
ov000_0220a514_Lc0:
    ldrb r0, [r8, #0x1e4]
    cmp r0, #2
    beq ov000_0220a514_L11c
    subs r0, r7, #102400
    mov r0, #0
    sbcs r0, r6, r0
    blt ov000_0220a514_Lfc
    add r0, r8, #112
    bl native_fn_021d8c18
    cmp r0, #0
    bne ov000_0220a514_Lfc
    mov r0, r4
    bl native_fn_0220a4e4
    cmp r0, #0
    beq ov000_0220a514_L11c
ov000_0220a514_Lfc:
    str r4, [r9]
    str r7, [r9, #0x8]
    str r6, [r9, #0xc]
    str r11, [r9, #0x10]
    mov r0, #2
    str r0, [r9, #0x4]
    add r9, r9, #20
    add r10, r10, #1
ov000_0220a514_L11c:
    add r4, r4, #1
    cmp r4, #48
    add r8, r8, #708
    blt ov000_0220a514_L28
    mov r0, r10
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
