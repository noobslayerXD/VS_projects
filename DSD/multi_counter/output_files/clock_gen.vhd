LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE work.ALL;

ENTITY clock_gen IS
    PORT (
        --inputs
        clk : IN STD_LOGIC;
        speed : IN STD_LOGIC;
        reset : IN STD_LOGIC;

        --outputs
        clk_out : OUT STD_LOGIC

    );
END clock_gen;

ARCHITECTURE clock_gen_impl OF clock_gen IS
    SIGNAL counter : INTEGER := 0;
    SIGNAL pulse : STD_LOGIC := '0';
    CONSTANT CLOCK_PERIOD_NS : INTEGER := 20; -- 50MHz clock period = 20ns
    CONSTANT SPEED_1_CYCLES : INTEGER := 50_000_000; -- 50MHz * 1s = 50,000,000 cycles
    CONSTANT SPEED_0_CYCLES : INTEGER := 250_000; -- 50MHz * 5ms = 250,000 cycles

BEGIN
    PROCESS (clk, reset)
    BEGIN
        IF reset = '0' THEN
            counter <= 0;
            pulse <= '0';
        ELSIF rising_edge(clk) THEN
            IF speed = '1' THEN
                -- Generate a pulse every second
                IF counter >= SPEED_1_CYCLES THEN
                    pulse <= '1';
                    counter <= 0;
                ELSE
                    pulse <= '0';
                    counter <= counter + 1;
                END IF;
            ELSIF speed = '0' THEN
                -- Generate a pulse every 5 milliseconds
                IF counter >= SPEED_0_CYCLES THEN
                    pulse <= '1';
                    counter <= 0;
                ELSE
                    pulse <= '0';
                    counter <= counter + 1;
                END IF;
            END IF;
        END IF;
    END PROCESS;

    clk_out <= pulse;

END clock_gen_impl;