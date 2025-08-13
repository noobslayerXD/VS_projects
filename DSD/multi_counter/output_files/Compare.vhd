LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY Compare IS
    PORT (
        tm_watch : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        tm_alarm : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        alarm : OUT STD_LOGIC
    );
END Compare;

ARCHITECTURE Compare_impl OF Compare IS
BEGIN
    PROCESS (tm_watch, tm_alarm)
    BEGIN
        IF tm_watch = tm_alarm THEN
            alarm <= '1';
        ELSE
            alarm <= '0';
        END IF;
    END PROCESS;
END Compare_impl;