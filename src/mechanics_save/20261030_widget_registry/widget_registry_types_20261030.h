#ifndef PRIVATE_WIDGET_REGISTRY_TYPES_20261030
#define PRIVATE_WIDGET_REGISTRY_TYPES_20261030
typedef unsigned char u8;
typedef unsigned int u32;
typedef struct RegistryWidget { u8 prefix[129]; u8 index; u8 remaining[14]; } RegistryWidget;
typedef struct RegistryManager { u8 prefix[0x3544]; u32 objects[128]; } RegistryManager;
extern RegistryManager native_data_020fbae8[];
#endif
