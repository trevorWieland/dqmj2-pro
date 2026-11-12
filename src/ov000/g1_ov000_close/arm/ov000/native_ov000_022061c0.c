/* ov000 row 0x022061c0: 180 bytes.
 *
 * What it does: 43 instructions; 13 call(s) to 0x0202a1e0, 0x0204157c, 0x020414c8, +10 more; loops (back edge at +0x08); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xac -> constant 0x02238248 (image word 0x02238248)
 *   pool +0xb0 -> constant 0x02238260 (image word 0x02238260)
 *   branch +0x68 -> +0x78
 *   branch +0x70 -> +0x8c
 *   branch +0x74 -> +0x9c
 *   branch +0x88 -> +0x9c
 *   test +0x64 cmp r0, #0
 *   test +0x6c cmp r0, #1
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022061c0; the literal pool and
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

extern void native_fn_0202a1e0(void);
extern void native_fn_0204157c(void);
extern void native_fn_020414c8(void);
extern void native_fn_020418b0(void);
extern void native_fn_02048e74(void);
extern void native_fn_02048e8c(void);
extern void native_fn_022063f8(void);
extern void native_fn_020c18a8(void);
extern void native_fn_020c18b8(void);
extern void native_fn_02207bc0(void);
extern void native_fn_020c1898(void);
extern void native_fn_0205e644(void);


asm u32 native_ov000_022061c0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #2
    bl native_fn_0202a1e0
    ldr r1, =0x02238248
    strb r0, [r1]
    mov r0, #0
    bl native_fn_0204157c
    mov r0, #63
    bl native_fn_020414c8
    mov r0, #2
    bl native_fn_020418b0
    ldr r0, =0x02238260
    mov r1, #6
    bl native_fn_02048e74
    bl native_fn_02048e8c
    bl native_fn_022063f8
    ldr r0, =0x02238248
    ldrsb r0, [r0]
    bl native_fn_0202a1e0
    ldr r0, =0x02238248
    mov r1, #1
    str r1, [r0, #0x4]
    mov r1, #0
    str r1, [r0, #0x1c]
    bl native_fn_020c18a8
    cmp r0, #0
    beq ov000_022061c0_L78
    cmp r0, #1
    beq ov000_022061c0_L8c
    b ov000_022061c0_L9c
ov000_022061c0_L78:
    ldr r1, =0x02238248
    mov r0, #0
    str r0, [r1, #0x18]
    bl native_fn_020c18b8
    b ov000_022061c0_L9c
ov000_022061c0_L8c:
    ldr r0, =0x02238248
    mov r1, #1
    str r1, [r0, #0x18]
    bl native_fn_02207bc0
ov000_022061c0_L9c:
    mov r0, #0
    bl native_fn_020c1898
    bl native_fn_0205e644
    ldmia sp!, {r3, pc}
}
