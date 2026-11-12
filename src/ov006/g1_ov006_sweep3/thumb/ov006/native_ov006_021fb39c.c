/* ov006 row 0x021fb39c: 120 bytes.
 *
 * What it does: 48 instructions; 12 call(s) to 0x021fe6e8, 0x021f2a4c, 0x021fb3b4, +9 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   branch +0x12 -> +0x18
 *   branch +0x16 -> +0x1a
 *   branch +0x2a -> +0x32
 *   branch +0x32 -> +0x42
 *   branch +0x48 -> +0x72
 *   test +0x10 cmp r1, #0x6
 *   test +0x28 cmp r4, #0x17
 *   test +0x46 cmp r4, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb39c; the literal pool and
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

extern void native_fn_021fe6e8(void);
extern void native_fn_021f2a4c(void);
extern void native_fn_020024bc(void);
extern void native_fn_021fabe4(void);
extern void native_fn_021fb080(void);
extern void native_fn_02026144(void);
extern void native_fn_021fe6d0(void);
extern void native_fn_021fe6d8(void);
extern void native_fn_021fb550(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_021fb39c (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r5, r0, #0x0
    bl native_fn_021fe6e8
    bl native_fn_021f2a4c
    ldr r0, =0x0221c0ec
    ldrh r1, [r0, #0x4]
    cmp r1, #0x6
    bls ov006_021fb39c_L18
    sub r1, r1, #0x6
    b ov006_021fb39c_L1a
ov006_021fb39c_L18:
    mov r1, #0x0
ov006_021fb39c_L1a:
    strh r1, [r0, #0x4]
    ldr r0, =0x0221c0ec
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_020024bc
    add r4, r0, #0x0
    cmp r4, #0x17
    bne ov006_021fb39c_L32
    bl native_fn_021fabe4
    pop {r3, r4, r5, pc}
ov006_021fb39c_L32:
    ble ov006_021fb39c_L42
    ldr r1, =0x0221c0ec
    mov r0, #0x1d
    ldrh r2, [r1, #0x4]
    sub r0, r0, r4
    mov r4, #0x0
    add r0, r2, r0
    strh r0, [r1, #0x4]
ov006_021fb39c_L42:
    bl native_fn_021fb080
    cmp r4, #0x0
    bne ov006_021fb39c_L72
    ldr r0, =0x0221c0ec
    ldrh r1, [r0, #0x4]
    mov r0, #0x37
    mul r0, r1
    mov r1, #0x91
    blx native_fn_02026144
    bl native_fn_021fe6d0
    bl native_fn_021fe6d8
    bl native_fn_021fb550
    ldr r1, =0x0221c0ec
    mov r0, #0x0
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    add r1, r5, #0x0
    bl native_fn_02204974
ov006_021fb39c_L72:
    pop {r3, r4, r5, pc}
}
