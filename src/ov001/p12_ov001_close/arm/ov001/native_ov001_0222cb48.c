/* ov001 row 0x0222cb48: 228 bytes.
 *
 * What it does: 55 instructions; 2 call(s) to 0x020c5968, 0x02044dc4; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (55 instructions, 2 calls, 17 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0xdc -> constant 0x02249828 (image word 0x02249828)
 *   pool +0xe0 -> constant 0x000001bd (image word 0x000001bd)
 *   branch +0x28 -> +0xc0
 *   branch +0x40 -> +0xc0
 *   branch +0x44 -> +0xc0
 *   branch +0x48 -> +0x6c
 *   branch +0x4c -> +0x6c
 *   branch +0x50 -> +0x6c
 *   branch +0x54 -> +0x6c
 *   branch +0x58 -> +0x6c
 *   branch +0x5c -> +0x6c
 *   branch +0x60 -> +0x80
 *   branch +0x64 -> +0xa4
 *   branch +0x68 -> +0xa4
 *   branch +0x7c -> +0xc0
 *   branch +0x8c -> +0xc0
 *   branch +0xa0 -> +0xc0
 *   branch +0xac -> +0xc0
 *   back edge +0xd0 -> +0x1c
 *   test +0x24 cmp r0, #0
 *   test +0x38 cmp r0, #9
 *   test +0x84 cmp r0, #100
 *   test +0x88 cmpne r0, #101
 *   test +0xa8 cmp r0, #101
 *   test +0xc8 cmp r4, r0, lsr #16
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222cb48; the literal pool and
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

extern void native_fn_020c5968(void);
extern void native_fn_02044dc4(void);


asm u32 native_ov001_0222cb48 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r7, #0
    ldr r5, =0x02249828
    ldr r4, =0x000001bd
    mov r9, r0
    mov r8, r7
    mov r6, r7
ov001_0222cb48_L1c:
    mov r0, r8
    bl native_fn_020c5968
    cmp r0, #0
    bne ov001_0222cb48_Lc0
    mov r0, r8
    mov r1, r6
    bl native_fn_02044dc4
    cmp r0, #9
    addls pc, pc, r0, lsl #2
    b ov001_0222cb48_Lc0
    b ov001_0222cb48_Lc0
    b ov001_0222cb48_L6c
    b ov001_0222cb48_L6c
    b ov001_0222cb48_L6c
    b ov001_0222cb48_L6c
    b ov001_0222cb48_L6c
    b ov001_0222cb48_L6c
    b ov001_0222cb48_L80
    b ov001_0222cb48_La4
    b ov001_0222cb48_La4
ov001_0222cb48_L6c:
    add r0, r7, #1
    mov r0, r0, lsl #16
    str r8, [r9, r7, lsl #2]
    mov r7, r0, lsr #16
    b ov001_0222cb48_Lc0
ov001_0222cb48_L80:
    ldrb r0, [r5]
    cmp r0, #100
    cmpne r0, #101
    bne ov001_0222cb48_Lc0
    add r0, r7, #1
    mov r0, r0, lsl #16
    str r8, [r9, r7, lsl #2]
    mov r7, r0, lsr #16
    b ov001_0222cb48_Lc0
ov001_0222cb48_La4:
    ldrb r0, [r5]
    cmp r0, #101
    bne ov001_0222cb48_Lc0
    add r0, r7, #1
    mov r0, r0, lsl #16
    str r8, [r9, r7, lsl #2]
    mov r7, r0, lsr #16
ov001_0222cb48_Lc0:
    add r0, r8, #1
    mov r0, r0, lsl #16
    cmp r4, r0, lsr #16
    mov r8, r0, lsr #16
    bhi ov001_0222cb48_L1c
    mov r0, r7
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
