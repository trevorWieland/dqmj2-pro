/* ov001 row 0x02223e54: 180 bytes.
 *
 * What it does: 45 instructions; 8 call(s) to 0x02044cdc, 0x021db8d0, 0x02218cf8, +5 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 8 calls (45 instructions, 8 calls, 4 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x68
 *   branch +0x38 -> +0x54
 *   back edge +0x60 -> +0x2c
 *   branch +0x64 -> +0x9c
 *   branch +0x74 -> +0x8c
 *   back edge +0x98 -> +0x68
 *   test +0x1c cmp r0, #2
 *   test +0x34 cmp r0, #0
 *   test +0x4c cmp r0, r7
 *   test +0x58 cmp r6, #3
 *   test +0x70 cmp r0, #0
 *   test +0x90 cmp r6, #3
 *   test +0xa4 cmp r7, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02223e54; the literal pool and
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

extern void native_fn_02044cdc(void);
extern void native_fn_021db8d0(void);
extern void native_fn_02218cf8(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_02223e54 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r5, [r0]
    ldr r8, [r0, #0x8]
    ldr r0, [r5, #0x1e8]
    mov r7, #0
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r0, #2
    mov r6, r7
    mov r4, #121
    beq ov001_02223e54_L68
ov001_02223e54_L2c:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02223e54_L54
    mov r0, r5
    mov r1, r8
    mov r2, r4
    bl native_fn_02218cf8
    cmp r0, r7
    movgt r7, r0
ov001_02223e54_L54:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    blt ov001_02223e54_L2c
    b ov001_02223e54_L9c
ov001_02223e54_L68:
    mov r0, r8
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02223e54_L8c
    mov r0, r5
    mov r1, r8
    mov r2, r4
    bl native_fn_02218cf8
    add r7, r7, r0
ov001_02223e54_L8c:
    add r6, r6, #1
    cmp r6, #3
    add r8, r8, #1088
    blt ov001_02223e54_L68
ov001_02223e54_L9c:
    mov r0, r5
    bl native_fn_021dbd24
    cmp r7, r0
    movge r0, #1
    movlt r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
