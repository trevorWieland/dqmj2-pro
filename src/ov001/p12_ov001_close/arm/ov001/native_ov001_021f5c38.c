/* ov001 row 0x021f5c38: 136 bytes.
 *
 * What it does: 34 instructions; 5 call(s) to 0x0207afec, 0x021db438, 0x021f5cb8, +2 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 5 calls (34 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x48
 *   branch +0x54 -> +0x80
 *   back edge +0x7c -> +0x58
 *   test +0x28 cmp r0, #1
 *   test +0x50 cmp r9, #0
 *   test +0x70 cmp r8, r9
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f5c38; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021db438(void);
extern void native_fn_021f5ac4(void);


asm u32 native_ov001_021f5c38 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r7, r0
    mov r0, r2
    mov r6, r1
    mov r5, r3
    bl native_fn_0207afec
    mov r4, r0
    ldrh r0, [r4, #8]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #28
    cmp r0, #1
    movne r9, #1
    bne ov001_021f5c38_L48
    ldrb r0, [r6, #0x31e]
    mov r1, #0
    bl native_fn_021db438
    mov r6, r0
    mov r9, #3
ov001_021f5c38_L48:
    mov r8, #0
    mov r10, r8
    cmp r9, #0
    ble ov001_021f5c38_L80
ov001_021f5c38_L58:
    ldrsh r2, [r4, #18]
    mov r0, r7
    mov r1, r6
    mov r3, r5
    bl native_fn_021f5ac4
    add r8, r8, #1
    cmp r8, r9
    add r10, r10, r0
    add r6, r6, #1088
    blt ov001_021f5c38_L58
ov001_021f5c38_L80:
    mov r0, r10
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
