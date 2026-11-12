/* ov006 row 0x021fd11c: 208 bytes.
 *
 * What it does: 77 instructions; 13 call(s) to 0x021fedc8, 0x021f5328, 0x021fd1ec, +10 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xb4 -> constant 0x0221c114 (image word 0x0221c114)
 *   pool +0xb8 -> native_data_0220b8f8 (image word 0x0220b8f8)
 *   pool +0xbc -> native_data_0220b940 (image word 0x0220b940)
 *   pool +0xc0 -> native_data_0220b944 (image word 0x0220b944)
 *   pool +0xc4 -> native_data_0220b942 (image word 0x0220b942)
 *   pool +0xc8 -> native_data_0220b946 (image word 0x0220b946)
 *   pool +0xcc -> native_fn_021fd284+1 (image word 0x021fd285)
 *   branch +0x12 -> +0x18
 *   branch +0x1e -> +0x3c
 *   branch +0x28 -> +0x2e
 *   branch +0x36 -> +0x3c
 *   test +0x10 cmp r1, #0x0
 *   test +0x1c cmp r0, #0x0
 *   test +0x26 cmp r0, #0x2
 *   test +0x34 cmp r0, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd11c; the literal pool and
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

extern void native_fn_021fedc8(void);
extern void native_fn_021f5328(void);
extern void native_fn_021fd1ec(void);
extern void native_fn_021f2b14(void);
extern u8 native_data_0220b8f8[];
extern void native_fn_021f26f0(void);
extern void native_fn_021f27fc(void);
extern void native_fn_021f5344(void);
extern u8 native_data_0220b940[];
extern u8 native_data_0220b944[];
extern u8 native_data_0220b942[];
extern u8 native_data_0220b946[];
extern void native_fn_021f29bc(void);
extern void native_fn_021fd284(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021fd11c (register u32 a0)
{
    push {r4, r5, r6, lr}
    bl native_fn_021fedc8
    add r4, r0, #0x0
    ldr r0, =0x0221c114
    mov r1, #0x0
    strb r1, [r0, #0x2]
    ldrsb r1, [r0, r1]
    cmp r1, #0x0
    bne ov006_021fd11c_L18
    mov r1, #0x1
    strb r1, [r0, #0]
ov006_021fd11c_L18:
    bl native_fn_021f5328
    cmp r0, #0x0
    beq ov006_021fd11c_L3c
    ldr r1, =0x0221c114
    mov r0, #0x1
    ldrsb r0, [r1, r0]
    cmp r0, #0x2
    bne ov006_021fd11c_L2e
    mov r0, #0x0
    strb r0, [r1, #0x1]
ov006_021fd11c_L2e:
    ldr r1, =0x0221c114
    mov r0, #0x0
    ldrsb r0, [r1, r0]
    cmp r0, #0x2
    bne ov006_021fd11c_L3c
    mov r0, #0x1
    strb r0, [r1, #0]
ov006_021fd11c_L3c:
    bl native_fn_021fd1ec
    bl native_fn_021f2b14
    bl native_fn_021f5328
    add r2, r0, #0x0
    ldr r1, =native_data_0220b8f8
    add r4, #0xf4
    ldrsb r1, [r1, r2]
    ldrb r2, [r4, #0]
    mov r0, #0x32
    add r2, r2, #0x1
    bl native_fn_021f26f0
    mov r0, #0x1
    bl native_fn_021f27fc
    mov r0, #0x1
    bl native_fn_021f5344
    add r5, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    add r4, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    add r6, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    lsl r1, r5, #0x5
    add r3, r0, #0x0
    ldr r0, =native_data_0220b940
    ldr r5, =0x0221c114
    mov r2, #0x1
    ldrsb r2, [r5, r2]
    add r0, r0, r1
    ldr r1, =native_data_0220b944
    lsl r5, r2, #0x3
    lsl r2, r4, #0x5
    add r1, r1, r2
    ldr r2, =native_data_0220b942
    lsl r4, r6, #0x5
    add r2, r2, r4
    lsl r4, r3, #0x5
    ldr r3, =native_data_0220b946
    ldrh r0, [r5, r0]
    add r3, r3, r4
    ldrh r1, [r5, r1]
    ldrh r2, [r5, r2]
    ldrh r3, [r5, r3]
    bl native_fn_021f29bc
    ldr r0, =native_fn_021fd284+1
    bl native_fn_021f52cc
    pop {r4, r5, r6, pc}
}
