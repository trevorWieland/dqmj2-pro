/* ov001 row 0x021e97c0: 196 bytes.
 *
 * What it does: 48 instructions; 8 call(s) to 0x0203d294, 0x021e97e8, 0x021db9e0, +5 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (48 instructions, 8 calls, 4 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xc0 -> constant 0x02238d7c (image word 0x02238d7c)
 *   branch +0x18 -> +0x28
 *   branch +0x38 -> +0x70
 *   branch +0x58 -> +0x88
 *   branch +0x6c -> +0x88
 *   branch +0x78 -> +0x88
 *   branch +0x8c -> +0xb8
 *   test +0x10 cmp r4, #50
 *   test +0x1c cmp r4, #75
 *   test +0x34 cmp r0, #0
 *   test +0x54 cmp r0, #40
 *   test +0x64 cmp r0, #0
 *   test +0x70 cmp r0, #1
 *   test +0x74 cmpeq r5, #2
 *   test +0x7c cmp r4, #25
 *   test +0x88 cmp r5, #3
 *   test +0x9c cmp r0, #0
 *   test +0xb0 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e97c0; the literal pool and
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

extern void native_fn_0203d294(void);
extern void native_fn_021db9e0(void);
extern void native_fn_021d9534(void);
extern void native_fn_021dbaac(void);


asm u32 native_ov001_021e97c0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r0, #100
    bl native_fn_0203d294
    mov r4, r0
    cmp r4, #50
    movlt r5, #2
    blt ov001_021e97c0_L28
    cmp r4, #75
    movlt r5, #3
    movge r5, #1
ov001_021e97c0_L28:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_021db9e0
    cmp r0, #0
    bne ov001_021e97c0_L70
    ldr r0, =0x02238d7c
    mov r1, #1
    ldr r0, [r0, #0x60]
    mov r2, r1
    mov r3, #0
    bl native_fn_021d9534
    cmp r0, #40
    ble ov001_021e97c0_L88
    mov r0, #3
    bl native_fn_0203d294
    cmp r0, #0
    moveq r5, #4
    b ov001_021e97c0_L88
ov001_021e97c0_L70:
    cmp r0, #1
    cmpeq r5, #2
    bne ov001_021e97c0_L88
    cmp r4, #25
    movlt r5, #3
    movge r5, #1
ov001_021e97c0_L88:
    cmp r5, #3
    bne ov001_021e97c0_Lb8
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_021dbaac
    cmp r0, #0
    ldr r0, =0x02238d7c
    movne r5, #2
    ldr r0, [r0, #0x54]
    bl native_fn_021dbaac
    cmp r0, #0
    movne r5, #2
ov001_021e97c0_Lb8:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
