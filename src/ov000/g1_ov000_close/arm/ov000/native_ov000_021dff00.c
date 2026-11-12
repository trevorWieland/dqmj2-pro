/* ov000 row 0x021dff00: 76 bytes.
 *
 * What it does: 18 instructions; 2 call(s) to 0x0203ca40, 0x021dff14; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x48 -> constant 0x02232264 (image word 0x02232264)
 *   branch +0x1c -> +0x30
 *   back edge +0x3c -> +0x14
 *   test +0x18 cmp r0, #0
 *   test +0x34 cmp r5, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dff00; the literal pool and
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

extern void native_fn_0203ca40(void);


asm u32 native_ov000_021dff00 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, #0
    ldr r7, =0x02232264
    mov r5, r6
    mov r4, r6
ov000_021dff00_L14:
    ldr r0, [r7]
    cmp r0, #0
    beq ov000_021dff00_L30
    mov r1, r4
    add r0, r7, #4
    bl native_fn_0203ca40
    add r6, r6, #1
ov000_021dff00_L30:
    add r5, r5, #1
    cmp r5, #4
    add r7, r7, #24
    blt ov000_021dff00_L14
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
