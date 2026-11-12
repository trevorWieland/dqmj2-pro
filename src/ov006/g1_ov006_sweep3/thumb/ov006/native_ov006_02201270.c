/* ov006 row 0x02201270: 80 bytes.
 *
 * What it does: 32 instructions; no calls; no back edge; returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x40 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0x44 -> native_data_0220e6ac (image word 0x0220e6ac)
 *   pool +0x48 -> native_data_0220e684 (image word 0x0220e684)
 *   pool +0x4c -> native_data_0220e6b4 (image word 0x0220e6b4)
 *   branch +0x0a -> +0x1e
 *   branch +0x28 -> +0x3c
 *   test +0x08 cmp r3, #0x0
 *   test +0x26 cmp r3, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02201270; the literal pool and
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

extern u8 native_data_0220e6ac[];
extern u8 native_data_0220e684[];
extern u8 native_data_0220e6b4[];


asm u32 native_ov006_02201270 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r2, =0x0221c164
    add r4, r0, #0x0
    ldr r3, [r2, #0]
    cmp r3, #0x0
    beq ov006_02201270_L1e
    ldr r2, [r2, #0x4]
    mov r0, #0x2
    ldr r2, [r2, #0x40]
    ldr r1, =native_data_0220e6ac
    lsl r5, r2, #0x2
    ldr r2, =native_data_0220e684
    lsl r0, r0, #0x1a
    ldr r2, [r2, r5]
    blx r3
ov006_02201270_L1e:
    ldr r2, =0x0221c164
    ldr r0, [r2, #0x4]
    str r4, [r0, #0x40]
    ldr r3, [r2, #0]
    cmp r3, #0x0
    beq ov006_02201270_L3c
    ldr r2, [r2, #0x4]
    mov r0, #0x2
    ldr r2, [r2, #0x40]
    ldr r1, =native_data_0220e6b4
    lsl r4, r2, #0x2
    ldr r2, =native_data_0220e684
    lsl r0, r0, #0x1a
    ldr r2, [r2, r4]
    blx r3
ov006_02201270_L3c:
    pop {r3, r4, r5, pc}
    mov r8, r8
}
