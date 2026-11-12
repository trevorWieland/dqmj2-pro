/* ov000 row 0x021e3948: 156 bytes.
 *
 * What it does: 38 instructions; 6 call(s) to 0x021e3444, 0x021e39d4, 0x021e3478, +3 more; loops (back edge at +0x0c); returns through pop {r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x98 -> constant 0x02234388 (image word 0x02234388)
 *   branch +0x14 -> +0x8c
 *   branch +0x78 -> +0x80
 *   test +0x10 cmp r0, #0
 *   test +0x74 cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e3948; the literal pool and
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

extern void native_fn_021e3444(void);
extern void native_fn_021e3478(void);
extern void native_fn_021e34b8(void);
extern void native_fn_021e7b08(void);


asm u32 native_ov000_021e3948 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #20
    mov r5, r0
    bl native_fn_021e3444
    cmp r0, #0
    blt ov000_021e3948_L8c
    ldr r2, =0x02234388
    mov r1, #52
    mla r4, r0, r1, r2
    mov r0, r4
    mov r1, r5
    mov r2, #1
    bl native_fn_021e3478
    mov r0, #0
    strb r0, [r4, #0x1e]
    strb r0, [r4, #0x1f]
    mov r3, #1
    strb r3, [r4, #0x1c]
    str r3, [sp]
    str r0, [sp, #0x4]
    str r0, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r1, #158
    mov r0, r4
    str r1, [sp, #0x10]
    mov r1, #3
    mov r2, #2
    bl native_fn_021e34b8
    ldrsh r0, [r4, #46]
    cmp r0, #0
    ble ov000_021e3948_L80
    bl native_fn_021e7b08
ov000_021e3948_L80:
    add sp, sp, #20
    mov r0, #1
    ldmia sp!, {r4, r5, pc}
ov000_021e3948_L8c:
    mov r0, #0
    add sp, sp, #20
    ldmia sp!, {r4, r5, pc}
}
