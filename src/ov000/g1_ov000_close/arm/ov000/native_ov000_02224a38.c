/* ov000 row 0x02224a38: 188 bytes.
 *
 * What it does: 46 instructions; 16 call(s) to 0x02062520, 0x01ffa988, 0x02061284, +13 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb8 -> constant 0x022468b8 (image word 0x022468b8)
 *   back edge +0x84 -> +0x54
 *   test +0x08 cmp r0, #0
 *   test +0x80 cmp r7, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02224a38; the literal pool and
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

extern void native_fn_02062520(void);
extern void native_fn_01ffa988(void);
extern void native_fn_02061284(void);
extern void native_fn_01ffae48(void);
extern void native_fn_01ffb340(void);
extern void native_fn_02049604(void);
extern void native_fn_022249b0(void);
extern void native_fn_02223ce0(void);
extern void native_fn_0206344c(void);
extern void native_fn_0206349c(void);
extern void native_fn_021f33ac(void);
extern void native_fn_021f33d4(void);
extern void native_fn_020620e8(void);
extern void native_fn_020cf73c(void);


asm u32 native_ov000_02224a38 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_02062520
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    bl native_fn_01ffa988
    ldr r1, =0x022468b8
    mov r0, #1
    str r0, [r1, #0x14]
    bl native_fn_02061284
    mov r0, #0
    mov r1, #2
    bl native_fn_01ffae48
    bl native_fn_01ffb340
    mov r1, #1
    bl native_fn_02049604
    bl native_fn_022249b0
    mov r7, #0
    mov r6, r7
    mov r5, #1
    mov r4, r7
ov000_02224a38_L54:
    mov r0, r6
    mov r1, r7
    mov r2, r6
    bl native_fn_02223ce0
    mov r0, r5
    mov r1, r7
    mov r2, r4
    bl native_fn_02223ce0
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #3
    blt ov000_02224a38_L54
    bl native_fn_0206344c
    bl native_fn_0206349c
    bl native_fn_021f33ac
    mov r0, #2
    bl native_fn_021f33d4
    mov r0, #19
    mov r1, #1
    bl native_fn_020620e8
    mov r0, #8
    bl native_fn_020cf73c
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
