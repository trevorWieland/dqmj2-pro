/* ov001 row 0x021f83a4: 252 bytes.
 *
 * What it does: 62 instructions; 6 call(s) to 0x021db8d0, 0x021f82d8, 0x021dc230, +3 more; loops (back edge at +0x18); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (62 instructions, 6 calls, 9 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0xf8 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x10 -> +0x54
 *   branch +0x20 -> +0x38
 *   branch +0x50 -> +0xf0
 *   branch +0x58 -> +0xa8
 *   branch +0xa4 -> +0xf0
 *   branch +0xac -> +0xd8
 *   branch +0xc4 -> +0xf0
 *   branch +0xd4 -> +0xf0
 *   branch +0xdc -> +0xf0
 *   test +0x0c cmp r1, #0
 *   test +0x1c cmp r0, #0
 *   test +0x54 cmp r1, #10
 *   test +0xa8 cmp r1, #20
 *   test +0xc0 cmp r0, #0
 *   test +0xd8 cmp r1, #100
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f83a4; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f82d8(void);
extern void native_fn_021dc230(void);
extern void native_fn_021db788(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f2230(void);


asm u32 native_ov001_021f83a4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x28]
    cmp r1, #0
    bne ov001_021f83a4_L54
    ldr r0, [r0, #0x78]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    bne ov001_021f83a4_L38
    ldr r0, =0x0223989c
    mov r1, #27
    strb r1, [r0, #0x1b]
    mov r0, #0
    ldmia sp!, {r4, pc}
ov001_021f83a4_L38:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x78]
    bl native_fn_021f82d8
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x28]
    b ov001_021f83a4_Lf0
ov001_021f83a4_L54:
    cmp r1, #10
    bne ov001_021f83a4_La8
    ldr r0, [r0, #0x78]
    mov r1, #1
    add r2, r0, #256
    ldrsh r4, [r2, #240]
    bl native_fn_021dc230
    ldr r0, =0x0223989c
    mov r1, #0
    ldr r0, [r0, #0x78]
    bl native_fn_021db788
    ldr r0, =0x0223989c
    mov r2, r4
    ldr r1, [r0, #0x78]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x28]
    b ov001_021f83a4_Lf0
ov001_021f83a4_La8:
    cmp r1, #20
    bne ov001_021f83a4_Ld8
    ldr r0, [r0, #0x78]
    mov r1, #0
    ldrb r2, [r0, #0x31e]
    bl native_fn_021f2230
    cmp r0, #0
    beq ov001_021f83a4_Lf0
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x28]
    b ov001_021f83a4_Lf0
ov001_021f83a4_Ld8:
    cmp r1, #100
    bne ov001_021f83a4_Lf0
    mov r1, #0
    strb r1, [r0, #0x28]
    mov r1, #27
    strb r1, [r0, #0x1b]
ov001_021f83a4_Lf0:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
