LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

-- Producing a synchronous edge-detect pulse for the leading and trailing
-- edges of a long (many clocks) asynchronous pulse.

ENTITY synch IS
  PORT (
    async_sig : IN STD_LOGIC;
    clk : IN STD_LOGIC;
    rise : OUT STD_LOGIC;
    fall : OUT STD_LOGIC);
END;

ARCHITECTURE RTL OF synch IS
BEGIN
  sync1 : PROCESS (clk)
    VARIABLE resync : STD_LOGIC_VECTOR(1 TO 3);
  BEGIN
    IF rising_edge(clk) THEN
      -- detect rising and falling edges.
      rise <= resync(2) AND NOT resync(3);
      fall <= resync(3) AND NOT resync(2);
      -- update history shifter.
      resync := async_sig & resync(1 TO 2);
    END IF;
  END PROCESS;

END ARCHITECTURE;