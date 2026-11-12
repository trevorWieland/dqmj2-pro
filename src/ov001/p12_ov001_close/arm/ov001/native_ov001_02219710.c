/* ov001 row 0x02219710: 96 bytes.
 *
 * What it does: 24 instructions; 5 call(s) to 0x021db8d0, 0x021dbd3c, 0x021dbd8c, +2 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 5 calls (24 instructions, 5 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x3c
 *   branch +0x38 -> +0x58
 *   back edge +0x54 -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x34 cmp r0, r4, lsl #1
 *   test +0x3c cmp r6, #2
 *   test +0x4c cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219710; the literal pool and
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
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbd8c(void);


asm u32 native_ov001_02219710 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r5, [r0]
    ldr r7, [r0, #0x8]
    mov r6, #0
ov001_02219710_L10:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02219710_L3c
    mov r0, r5
    bl native_fn_021dbd3c
    mov r4, r0
    mov r0, r7
    bl native_fn_021dbd8c
    cmp r0, r4, lsl #1
    blt ov001_02219710_L58
ov001_02219710_L3c:
    cmp r6, #2
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_02219710_L10
ov001_02219710_L58:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
