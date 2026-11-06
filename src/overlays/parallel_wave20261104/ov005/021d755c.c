typedef struct Object Object;
typedef struct Interface Interface;
typedef struct Methods Methods;
struct Methods {
    unsigned char pad[20];
    int (*operation)(Object *, int);
};
struct Interface {
    unsigned int reserved[2];
    void (*notify)(int, void *);
    Methods *methods;
};
struct Object {
    unsigned char pad[32];
    Interface *interface;
};
int native_ov005_021d755c(Object *object, int argument)
{
    int result = object->interface->methods->operation(object, argument);
    if (result && object->interface->notify)
        object->interface->notify(5, (unsigned char *)object + 16);
    return result;
}
