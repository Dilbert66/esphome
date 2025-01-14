import esphome.codegen as cg
from esphome.components import spi
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_MODE

DEPENDENCIES = ["spi"]
CODEOWNERS = ["@clydebarrow"]

MULTI_CONF = True
spi_device_ns = cg.esphome_ns.namespace("spi_device")

spi_device = spi_device_ns.class_("SPIDeviceComponent", cg.Component, spi.SPIDevice)

BitOrder = spi.spi_ns.enum("SPIBitOrder")
ORDERS = {
    "msb_first": BitOrder.BIT_ORDER_MSB_FIRST,
    "lsb_first": BitOrder.BIT_ORDER_LSB_FIRST,
}
CONF_BIT_ORDER = "bit_order"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ID): cv.declare_id(spi_device),
        cv.Optional(CONF_BIT_ORDER, default="msb_first"): cv.enum(ORDERS, lower=True),
        cv.Optional(CONF_MODE): cv.invalid(
            "The 'mode' option has been renamed to 'spi_mode'."
        ),
    }
).extend(spi.spi_device_schema(False, "1MHz"))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_bit_order(config[CONF_BIT_ORDER]))
    await spi.register_spi_device(var, config)
