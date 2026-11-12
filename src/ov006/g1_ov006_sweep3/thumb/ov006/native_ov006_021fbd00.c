/* ov006 row 0x021fbd00: 88 bytes.
 *
 * What it does: 31 instructions; 7 call(s) to 0x021f5740, 0x021f52cc, 0x021ff718, +4 more; loops (back edge at +0x02); returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x4c -> constant 0x0221c0f8 (image word 0x0221c0f8)
 *   pool +0x50 -> native_fn_021fbc1c+1 (image word 0x021fbc1d)
 *   pool +0x54 -> native_fn_021fbd58+1 (image word 0x021fbd59)
 *   branch +0x08 -> +0x10
 *   branch +0x0c -> +0x1e
 *   test +0x06 cmp r0, #0x2
 *   test +0x0a cmp r0, #0x4
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fbd00; the literal pool and
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

extern void native_fn_021f5740(void);
extern void native_fn_021fbc1c(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021ff718(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_02200344(void);
extern void native_fn_021f23f4(void);
extern void native_fn_021fbd58(void);


asm u32 native_ov006_021fbd00 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f5740
    cmp r0, #0x2
    beq ov006_021fbd00_L10
    cmp r0, #0x4
    beq ov006_021fbd00_L1e
    pop {r3, pc}
ov006_021fbd00_L10:
    ldr r0, =0x0221c0f8
    mov r1, #0x1
    strb r1, [r0, #0]
    ldr r0, =native_fn_021fbc1c+1
    bl native_fn_021f52cc
    pop {r3, pc}
ov006_021fbd00_L1e:
    ldr r0, =0x0221c0f8
    mov r1, #0x0
    strb r1, [r0, #0]
    bl native_fn_021ff718
    mov r0, #0x9
    bl native_fn_021ff6d4
    mov r1, #0x1
    mov r0, #0x0
    str r0, [sp]
    mov r0, #0xd
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    bl native_fn_021f23f4
    ldr r0, =native_fn_021fbd58+1
    bl native_fn_021f52cc
    pop {r3, pc}
    mov r8, r8
}
