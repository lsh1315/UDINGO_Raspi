################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/DWM_functions.c \
../Core/Src/deca_device.c \
../Core/Src/deca_mutex.c \
../Core/Src/deca_params_init.c \
../Core/Src/deca_timestamps.c \
../Core/Src/ds_initiator.c \
../Core/Src/ds_responder.c \
../Core/Src/leds.c \
../Core/Src/main.c \
../Core/Src/port.c \
../Core/Src/position_detection.c \
../Core/Src/ss_initiator.c \
../Core/Src/ss_responder.c \
../Core/Src/stm32f1xx_hal_msp.c \
../Core/Src/stm32f1xx_it.c \
../Core/Src/syscalls.c \
../Core/Src/sysmem.c \
../Core/Src/system_stm32f1xx.c 

OBJS += \
./Core/Src/DWM_functions.o \
./Core/Src/deca_device.o \
./Core/Src/deca_mutex.o \
./Core/Src/deca_params_init.o \
./Core/Src/deca_timestamps.o \
./Core/Src/ds_initiator.o \
./Core/Src/ds_responder.o \
./Core/Src/leds.o \
./Core/Src/main.o \
./Core/Src/port.o \
./Core/Src/position_detection.o \
./Core/Src/ss_initiator.o \
./Core/Src/ss_responder.o \
./Core/Src/stm32f1xx_hal_msp.o \
./Core/Src/stm32f1xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32f1xx.o 

C_DEPS += \
./Core/Src/DWM_functions.d \
./Core/Src/deca_device.d \
./Core/Src/deca_mutex.d \
./Core/Src/deca_params_init.d \
./Core/Src/deca_timestamps.d \
./Core/Src/ds_initiator.d \
./Core/Src/ds_responder.d \
./Core/Src/leds.d \
./Core/Src/main.d \
./Core/Src/port.d \
./Core/Src/position_detection.d \
./Core/Src/ss_initiator.d \
./Core/Src/ss_responder.d \
./Core/Src/stm32f1xx_hal_msp.d \
./Core/Src/stm32f1xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32f1xx.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o Core/Src/%.su Core/Src/%.cyclo: ../Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F103xB -c -I../Core/Inc -I../Drivers/STM32F1xx_HAL_Driver/Inc/Legacy -I../Drivers/STM32F1xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/DWM_functions.cyclo ./Core/Src/DWM_functions.d ./Core/Src/DWM_functions.o ./Core/Src/DWM_functions.su ./Core/Src/deca_device.cyclo ./Core/Src/deca_device.d ./Core/Src/deca_device.o ./Core/Src/deca_device.su ./Core/Src/deca_mutex.cyclo ./Core/Src/deca_mutex.d ./Core/Src/deca_mutex.o ./Core/Src/deca_mutex.su ./Core/Src/deca_params_init.cyclo ./Core/Src/deca_params_init.d ./Core/Src/deca_params_init.o ./Core/Src/deca_params_init.su ./Core/Src/deca_timestamps.cyclo ./Core/Src/deca_timestamps.d ./Core/Src/deca_timestamps.o ./Core/Src/deca_timestamps.su ./Core/Src/ds_initiator.cyclo ./Core/Src/ds_initiator.d ./Core/Src/ds_initiator.o ./Core/Src/ds_initiator.su ./Core/Src/ds_responder.cyclo ./Core/Src/ds_responder.d ./Core/Src/ds_responder.o ./Core/Src/ds_responder.su ./Core/Src/leds.cyclo ./Core/Src/leds.d ./Core/Src/leds.o ./Core/Src/leds.su ./Core/Src/main.cyclo ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/main.su ./Core/Src/port.cyclo ./Core/Src/port.d ./Core/Src/port.o ./Core/Src/port.su ./Core/Src/position_detection.cyclo ./Core/Src/position_detection.d ./Core/Src/position_detection.o ./Core/Src/position_detection.su ./Core/Src/ss_initiator.cyclo ./Core/Src/ss_initiator.d ./Core/Src/ss_initiator.o ./Core/Src/ss_initiator.su ./Core/Src/ss_responder.cyclo ./Core/Src/ss_responder.d ./Core/Src/ss_responder.o ./Core/Src/ss_responder.su ./Core/Src/stm32f1xx_hal_msp.cyclo ./Core/Src/stm32f1xx_hal_msp.d ./Core/Src/stm32f1xx_hal_msp.o ./Core/Src/stm32f1xx_hal_msp.su ./Core/Src/stm32f1xx_it.cyclo ./Core/Src/stm32f1xx_it.d ./Core/Src/stm32f1xx_it.o ./Core/Src/stm32f1xx_it.su ./Core/Src/syscalls.cyclo ./Core/Src/syscalls.d ./Core/Src/syscalls.o ./Core/Src/syscalls.su ./Core/Src/sysmem.cyclo ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/sysmem.su ./Core/Src/system_stm32f1xx.cyclo ./Core/Src/system_stm32f1xx.d ./Core/Src/system_stm32f1xx.o ./Core/Src/system_stm32f1xx.su

.PHONY: clean-Core-2f-Src

