/* ov000 row 0x021e824c: 232 bytes.
 *
 * What it does: 58 instructions; 6 call(s) to 0x021e7d18, 0x021e5ed8, 0x02042bfc, +3 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x3c
 *   branch +0x48 -> +0xd0
 *   branch +0x9c -> +0xc4
 *   branch +0xac -> +0xc4
 *   test +0x0c cmp r1, #0
 *   test +0x44 tst r0, #3
 *   test +0xa8 cmp r0, #255
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e824c; the literal pool and
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

extern void native_fn_021e7d18(void);
extern void native_fn_021e5ed8(void);
extern void native_fn_02042bfc(void);
extern void native_fn_021e5ef4(void);
extern void native_fn_021e5f10(void);
extern void native_fn_020420c4(void);


asm u32 native_ov000_021e824c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r1, [r5, #0x2a8]
    cmp r1, #0
    bne ov000_021e824c_L3c
    mov r1, #1
    mov r2, #0
    bl native_fn_021e7d18
    ldrb r0, [r5, #0x279]
    bl native_fn_021e5ed8
    ldr r1, [r0]
    mov r0, r5
    bl native_fn_02042bfc
    mov r0, #10
    strb r0, [r5, #0x2a8]
ov000_021e824c_L3c:
    add r0, r5, #512
    ldrsh r0, [r0, #172]
    tst r0, #3
    bne ov000_021e824c_Ld0
    ldrb r0, [r5, #0x279]
    bl native_fn_021e5ef4
    mov r4, r0
    ldr r1, [r5, #0x74]
    ldr r0, [r4, #0x4]
    ldr r3, [r5, #0x70]
    sub r12, r1, r0
    ldr r1, [r4]
    smull r0, r2, r12, r12
    sub r1, r3, r1
    smlal r0, r2, r1, r1
    ldr r12, [r5, #0x78]
    ldr r3, [r4, #0x8]
    mov r1, #0
    sub r3, r12, r3
    smlal r0, r2, r3, r3
    mov r0, r0, lsr #12
    orr r0, r0, r2, lsl #20
    subs r0, r0, #4096
    rscs r0, r1, r2, asr #12
    bge ov000_021e824c_Lc4
    ldrb r0, [r5, #0x279]
    bl native_fn_021e5f10
    cmp r0, #255
    beq ov000_021e824c_Lc4
    mov r1, #0
    strb r1, [r5, #0x2a8]
    strb r0, [r5, #0x279]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov000_021e824c_Lc4:
    mov r0, r5
    mov r1, r4
    bl native_fn_020420c4
ov000_021e824c_Ld0:
    add r1, r5, #512
    ldrsh r2, [r1, #172]
    mov r0, #0
    add r2, r2, #1
    strh r2, [r1, #172]
    ldmia sp!, {r3, r4, r5, pc}
}
