/* ov000 row 0x0222a4f4: 452 bytes.
 *
 * What it does: 107 instructions; 14 call(s) to 0x0203d0fc, 0x0203d0fc, 0x02003bb4, +11 more; loops (back edge at +0x04); returns through pop {r4, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1ac -> constant 0x02247568 (image word 0x02247568)
 *   pool +0x1b0 -> constant 0x04000304 (image word 0x04000304)
 *   pool +0x1b4 -> constant 0x80330010 (image word 0x80330010)
 *   pool +0x1b8 -> constant 0x04000064 (image word 0x04000064)
 *   pool +0x1bc -> constant 0x04001000 (image word 0x04001000)
 *   pool +0x1c0 -> constant 0x80320010 (image word 0x80320010)
 *   branch +0x10 -> +0x20
 *   branch +0x30 -> +0xf8
 *   branch +0xa8 -> +0x174
 *   branch +0xf4 -> +0x174
 *   test +0x08 cmp r0, #1
 *   test +0x18 cmp r0, #2
 *   test +0x2c cmp r0, #0
 *   test +0x9c cmp r1, #0
 *   test +0x17c cmp r0, #0
 *   test +0x194 cmp r0, #2
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222a4f4; the literal pool and
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

extern void native_fn_0203d0fc(void);
extern void native_fn_02003bb4(void);
extern void native_fn_020038a8(void);
extern void native_fn_02003888(void);
extern void native_fn_02002c98(void);
extern void native_fn_02002d00(void);
extern void native_fn_02003ba0(void);
extern void native_fn_02003950(void);
extern void native_fn_02041774(void);


asm u32 native_ov000_0222a4f4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    bl native_fn_0203d0fc
    cmp r0, #1
    moveq r4, #0
    beq ov000_0222a4f4_L20
    bl native_fn_0203d0fc
    cmp r0, #2
    moveq r4, #1
ov000_0222a4f4_L20:
    ldr r0, =0x02247568
    ldr r1, =0x04000304
    ldrb r0, [r0]
    cmp r0, #0
    beq ov000_0222a4f4_Lf8
    ldrh r0, [r1]
    orr r0, r0, #32768
    strh r0, [r1]
    bl native_fn_02003bb4
    mov r0, #4
    bl native_fn_020038a8
    mov r0, #8
    bl native_fn_02003888
    ldr r1, =0x80330010
    mov r0, #1
    orr r4, r1, r4, lsl #24
    ldr r3, =0x04000064
    mov r2, r0
    mov r1, #0
    str r4, [r3]
    bl native_fn_02002c98
    mov r2, #67108864
    ldr r1, [r2]
    ldr r0, =0x02247568
    bic r1, r1, #7936
    orr r1, r1, #256
    str r1, [r2]
    ldrh r1, [r2, #8]
    bic r1, r1, #3
    strh r1, [r2, #8]
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    movne r1, #0
    strneb r1, [r0, #0x1]
    bne ov000_0222a4f4_L174
    mov r0, #5
    bl native_fn_02002d00
    ldr r1, =0x04001000
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #1024
    str r0, [r1]
    ldrh r0, [r1, #12]
    and r0, r0, #67
    orr r0, r0, #132
    orr r0, r0, #16384
    strh r0, [r1, #12]
    ldrh r0, [r1, #12]
    bic r0, r0, #3
    strh r0, [r1, #12]
    ldrh r0, [r1, #12]
    bic r0, r0, #64
    strh r0, [r1, #12]
    b ov000_0222a4f4_L174
ov000_0222a4f4_Lf8:
    ldrh r0, [r1]
    bic r0, r0, #32768
    strh r0, [r1]
    bl native_fn_02003ba0
    mov r0, #8
    bl native_fn_02003950
    mov r0, #4
    bl native_fn_02003888
    ldr r1, =0x80320010
    mov r0, #1
    orr r4, r1, r4, lsl #24
    ldr r3, =0x04000064
    mov r2, r0
    mov r1, #0
    str r4, [r3]
    bl native_fn_02002c98
    mov r2, #67108864
    ldr r1, [r2]
    mov r0, #5
    bic r1, r1, #7936
    orr r1, r1, #256
    str r1, [r2]
    ldrh r1, [r2, #8]
    bic r1, r1, #3
    strh r1, [r2, #8]
    bl native_fn_02002d00
    ldr r1, =0x04001000
    ldr r0, [r1]
    bic r0, r0, #7936
    orr r0, r0, #4096
    str r0, [r1]
ov000_0222a4f4_L174:
    ldr r0, =0x02247568
    ldrb r0, [r0]
    cmp r0, #0
    moveq r1, #1
    ldr r0, =0x02247568
    movne r1, #0
    strb r1, [r0]
    bl native_fn_0203d0fc
    cmp r0, #2
    ldmneia sp!, {r4, pc}
    ldr r0, =0x02247568
    ldrb r0, [r0]
    bl native_fn_02041774
    ldmia sp!, {r4, pc}
}
