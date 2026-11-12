/* ov000 row 0x0222a814: 112 bytes.
 *
 * What it does: 27 instructions; 2 call(s) to 0x0222a884, 0x0222a91c; no back edge; returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x6c -> constant 0x022475ec (image word 0x022475ec)
 *   branch +0x14 -> +0x34
 *   branch +0x1c -> +0x44
 *   branch +0x30 -> +0x64
 *   branch +0x40 -> +0x64
 *   branch +0x4c -> +0x64
 *   test +0x10 cmp r0, #0
 *   test +0x18 cmp r0, #1
 *   test +0x20 cmp r0, #2
 *   test +0x48 cmp r0, r5
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222a814; the literal pool and
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

extern void native_fn_0222a884(void);
extern void native_fn_0222a91c(void);


asm u32 native_ov000_0222a814 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =0x022475ec
    ldr r0, [r4, #0x4]
    ldr r5, [r4]
    cmp r0, #0
    beq ov000_0222a814_L34
    cmp r0, #1
    beq ov000_0222a814_L44
    cmp r0, #2
    moveq r0, #0
    ldreq r5, [r4, #0x8]
    streq r0, [r4, #0x4]
    b ov000_0222a814_L64
ov000_0222a814_L34:
    bl native_fn_0222a884
    mov r0, #1
    str r0, [r4, #0x4]
    b ov000_0222a814_L64
ov000_0222a814_L44:
    bl native_fn_0222a91c
    cmp r0, r5
    beq ov000_0222a814_L64
    ldr r2, [r4]
    mov r1, #2
    str r2, [r4, #0xc]
    str r1, [r4, #0x4]
    str r0, [r4, #0x8]
ov000_0222a814_L64:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
