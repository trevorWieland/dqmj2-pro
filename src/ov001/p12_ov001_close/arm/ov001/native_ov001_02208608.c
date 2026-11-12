/* ov001 row 0x02208608: 104 bytes.
 *
 * What it does: 26 instructions; 2 call(s) to 0x02208668, 0x020877bc; loops (back edge at +0x40); returns through pop {r3, pc}
 *
 * Decoded shape: loop with 2 calls (26 instructions, 2 calls, 3 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x10 -> +0x48
 *   branch +0x20 -> +0x60
 *   back edge +0x40 -> +0x28
 *   branch +0x44 -> +0x60
 *   test +0x04 cmp r0, #1
 *   test +0x0c cmpeq r0, #0
 *   test +0x1c cmp r12, #0
 *   test +0x38 cmp r12, r0, asr #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208608; the literal pool and
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

extern void native_fn_020877bc(void);


asm u32 native_ov001_02208608 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #1
    ldreq r0, [sp, #0xc]
    cmpeq r0, #0
    bne ov001_02208608_L48
    ldrb r12, [sp, #0x8]
    mov r1, #0
    cmp r12, #0
    ble ov001_02208608_L60
    mov r3, #63
ov001_02208608_L28:
    add r0, r1, #1
    mov r1, r1, lsl #1
    mov r0, r0, lsl #24
    strh r3, [r2, r1]
    cmp r12, r0, asr #24
    mov r1, r0, asr #24
    bgt ov001_02208608_L28
    b ov001_02208608_L60
ov001_02208608_L48:
    mov r0, r1
    mov r1, r2
    mov r2, r3
    ldrb r3, [sp, #0x8]
    bl native_fn_020877bc
    mov r2, r0
ov001_02208608_L60:
    mov r0, r2
    ldmia sp!, {r3, pc}
}
