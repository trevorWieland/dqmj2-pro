/* ov000 row 0x0222a24c: 584 bytes.
 *
 * What it does: 139 instructions; 30 call(s) to 0x020481b8, 0x0204820c, 0x02048308, +27 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x22c -> constant 0x0400000a (image word 0x0400000a)
 *   pool +0x230 -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x234 -> constant 0x07000400 (image word 0x07000400)
 *   pool +0x238 -> constant 0x02247574 (image word 0x02247574)
 *   pool +0x23c -> constant 0xc0000c00 (image word 0xc0000c00)
 *   pool +0x240 -> constant 0x02247568 (image word 0x02247568)
 *   pool +0x244 -> constant 0x55555556 (image word 0x55555556)
 *   back edge +0x104 -> +0xf0
 *   back edge +0x154 -> +0x128
 *   back edge +0x164 -> +0x118
 *   branch +0x190 -> +0x1dc
 *   branch +0x1d8 -> +0x1f4
 *   test +0x100 cmp r2, #12
 *   test +0x148 cmp r2, #256
 *   test +0x15c cmp r3, #192
 *   test +0x188 cmp r4, #1
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222a24c; the literal pool and
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

extern void native_fn_020481b8(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_02003d68(void);
extern void native_fn_02003cf8(void);
extern void native_fn_02003d0c(void);
extern void native_fn_02003dcc(void);
extern void native_fn_02003de0(void);
extern void native_fn_0202abd8(void);
extern void native_fn_020033e8(void);
extern void native_fn_020035c0(void);
extern void native_fn_02002e5c(void);
extern void native_fn_02002c98(void);
extern void native_fn_02008c58(void);
extern void native_fn_02007308(void);
extern void native_fn_02004a50(void);
extern void native_fn_0203d0e4(void);
extern void native_fn_02028374(void);
extern void native_fn_0200235c(void);
extern void native_fn_0202834c(void);
extern void native_fn_02028334(void);
extern void native_fn_020282a8(void);
extern void native_fn_020414c8(void);


asm u32 native_ov000_0222a24c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r5, #0
    mov r4, r0
    add r0, sp, #0
    mov r1, r5
    mov r2, #2
    strh r5, [sp]
    bl native_fn_020481b8
    add r0, sp, #0
    mov r1, r5
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    bl native_fn_02003d68
    bl native_fn_02003cf8
    bl native_fn_02003d0c
    bl native_fn_02003dcc
    bl native_fn_02003de0
    mov r0, #2
    mov r1, #65536
    bl native_fn_0202abd8
    mov r0, #3
    bl native_fn_020033e8
    mov r0, #16
    bl native_fn_020035c0
    mov r0, #96
    bl native_fn_02002e5c
    mov r0, #1
    mov r1, r5
    mov r2, r0
    bl native_fn_02002c98
    ldr r7, =0x0400000a
    ldr r6, =0x04001000
    ldrh r2, [r7]
    mov r0, r5
    mov r1, #100663296
    and r2, r2, #67
    orr r2, r2, #3584
    strh r2, [r7]
    ldrh r3, [r7, #2]
    mov r2, #524288
    and r3, r3, #67
    orr r3, r3, #3840
    strh r3, [r7, #2]
    ldr r3, [r6]
    bic r3, r3, #96
    orr r3, r3, #32
    str r3, [r6]
    bl native_fn_02008c58
    mov r0, r5
    mov r1, #104857600
    mov r2, #262144
    bl native_fn_02008c58
    ldr r1, =0x07000400
    mov r0, #192
    mov r2, #1024
    bl native_fn_02008c58
    ldr r1, =0x02247574
    mov r2, r5
    mov r3, r5
ov000_0222a24c_Lf0:
    str r3, [r1, r2, lsl #3]
    add r0, r1, r2, lsl #3
    add r2, r2, #1
    str r3, [r0, #0x4]
    cmp r2, #12
    blt ov000_0222a24c_Lf0
    ldr r0, =0x02247574
    ldr r7, =0xc0000c00
    mov r12, r3
    mov r1, #0
ov000_0222a24c_L118:
    and r6, r3, #255
    mov r2, r1
    mov lr, r1
    orr r6, r6, r7
ov000_0222a24c_L128:
    mov r8, r2, lsl #23
    add r9, lr, r12, lsl #5
    orr r8, r6, r8, lsr #7
    add r2, r2, #64
    str r8, [r0, r5, lsl #3]
    add r8, r0, r5, lsl #3
    orr r9, r9, #61440
    strh r9, [r8, #4]
    cmp r2, #256
    add lr, lr, #8
    add r5, r5, #1
    blt ov000_0222a24c_L128
    add r3, r3, #64
    cmp r3, #192
    add r12, r12, #8
    blt ov000_0222a24c_L118
    mov r1, #96
    bl native_fn_02007308
    ldr r0, =0x02247574
    mov r1, #0
    mov r2, #96
    bl native_fn_02004a50
    mov r0, r4
    bl native_fn_0203d0e4
    cmp r4, #1
    mov r0, #0
    bne ov000_0222a24c_L1dc
    bl native_fn_02028374
    mov r1, #8192
    bl native_fn_0200235c
    mov r1, r0
    mov r0, #0
    bl native_fn_0202834c
    ldr r1, =0x02247568
    str r0, [r1, #0x4]
    mov r0, #0
    bl native_fn_02028334
    ldr r2, =0x55555556
    mov r3, r0, lsl #2
    smull r0, r1, r2, r3
    add r1, r1, r3, lsr #31
    mov r0, #0
    bl native_fn_020282a8
    ldr r1, =0x02247568
    b ov000_0222a24c_L1f4
ov000_0222a24c_L1dc:
    bl native_fn_02028374
    ldr r1, =0x02247568
    str r0, [r1, #0x4]
    mov r0, #0
    bl native_fn_02028334
    ldr r1, =0x02247568
ov000_0222a24c_L1f4:
    str r0, [r1, #0x8]
    ldr r1, =0x02247568
    mov r2, #1
    mov r0, #63
    strb r2, [r1]
    bl native_fn_020414c8
    ldr r3, =0x04001000
    ldr r0, =0x02247568
    ldr r2, [r3]
    mov r1, #1
    bic r2, r2, #7936
    str r2, [r3]
    strb r1, [r0, #0x1]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
