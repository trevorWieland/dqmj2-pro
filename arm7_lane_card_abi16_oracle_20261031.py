import arm7_lane_card_service_oracle_20261031 as service
import arm7_lane_card_init_oracle_20261031 as initialization
import arm7_lane_card_callbacks_oracle_20261031 as callbacks
import arm7_lane_card_pages_oracle_20261031 as pages


def oracle(original,rebuilt,address):
    if address==0x03802624:return initialization.oracle(original,rebuilt,address)
    if address in (0x038028e4,0x03802924,0x03802974):return callbacks.oracle(original,rebuilt,address)
    if address in (0x03802b70,0x03802c28):return pages.oracle(original,rebuilt,address)
    return service.oracle(original,rebuilt,address)
